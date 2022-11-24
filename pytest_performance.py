import asyncio
import time
from typing import Any, Awaitable, Callable, Union

import numpy as np
import pint
import pytest

SKIP_FLAG = '--performance-skip'
ureg = pint.UnitRegistry()


def pytest_addoption(parser):
    group = parser.getgroup('performance')
    group.addoption(
        SKIP_FLAG,
        action='store_true',
        help='Disable performance fixture'
    )


class PerformanceException(Exception):

    def __init__(self, func_name, expected_time, actual_time):
        super(PerformanceException, self).__init__(
            '\n'.join([
                'Function "{}" too slow!'.format(func_name),
                'Expected execution time: {:~}'.format(expected_time),
                'Actual execution time: {:~.5f}'.format(actual_time),
            ])
        )


class PerformanceFixture:

    @staticmethod
    def _profile(func, *args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        return result, end - start

    def _compare_to_target(self, actual):
        func_time_unit = actual.to(self._unit)
        if func_time_unit > self._target:
            raise PerformanceException(
                    self._func_name, self._target, func_time_unit
            )

    def __call__(
            self, func, *args,
            target=1000, unit=ureg.ms, iterations=10000,
            **kwargs
    ):
        self._unit = ureg.parse_expression(str(unit))
        self._target = target * self._unit
        self._func_name = func.__name__

        # Run func once to estimate overall test running time
        # Fail if first run is slower than target
        result, dur = self._profile(func, *args, **kwargs)
        func_time_s = dur * ureg.s
        self._compare_to_target(func_time_s)

        # Run the remaining iterations
        times = [dur]
        times.extend(
            [
                self._profile(func, *args, **kwargs)[1]
                for _ in range(1, iterations)
            ]
        )
        mean_time = np.mean(np.ascontiguousarray(times)) * ureg.s
        self._compare_to_target(mean_time)

        return result


@pytest.fixture(scope="function")
def performance(request):
    skip = request.config.getoption(SKIP_FLAG)
    if not skip:
        return PerformanceFixture()
    pytest.skip(f"Performance checks are skipped ({SKIP_FLAG} was used).")


AsyncFunc = Callable[[Any, Any], Awaitable[Any]]


class AsyncPerformanceFixture:
    @staticmethod
    async def _profile(func, *args, **kwargs):
        start = time.time()
        result = await func(*args, **kwargs)
        end = time.time()
        return result, end - start

    def _compare_to_target(self, actual):
        func_time_unit = actual.to(self._unit)
        if func_time_unit > self._target:
            raise PerformanceException(
                    self._func_name, self._target, func_time_unit
            )

    async def __call__(self, func: AsyncFunc, *args: Any,
                       target: int = 1000,
                       unit: Union[pint.Quantity, str] = ureg.ms,
                       iterations: int = 10000,
                       parallellizable: bool = True,
                       **kwargs: Any):
        self._unit = ureg.parse_expression(str(unit))
        self._target = target * self._unit
        self._func_name = func.__name__

        # Run func once to estimate overall test running time
        # Fail if first run is slower than target
        result, dur = await self._profile(func, *args, **kwargs)
        func_time_s = dur * ureg.s
        self._compare_to_target(func_time_s)

        # Run the remaining iterations
        if parallellizable:
            results = await asyncio.gather(*[
                self._profile(func, *args, **kwargs)
                for _ in range(1, iterations)
            ])
        else:
            results = []
            for _ in range(1, iterations):
                results.append(await self._profile(func, *args, **kwargs))

        times = [dur] + [res[1] for res in results]

        mean_time = np.mean(np.ascontiguousarray(times)) * ureg.s
        self._compare_to_target(mean_time)

        return result


@pytest.fixture(scope="function")
def async_performance(request):
    skip = request.config.getoption(SKIP_FLAG)
    if not skip:
        return AsyncPerformanceFixture()
    else:
        pytest.skip(f"Performance checks are skipped ({SKIP_FLAG} was used).")
