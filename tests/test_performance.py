# -*- coding: utf-8 -*-
from _pytest.config import ExitCode

from pytest_performance import SKIP_FLAG


def test_performance(testdir):
    # Given
    testdir.makepyfile("""        
        def foo():
            return 1

        def test_sth(performance):
            assert 1 == performance(foo, unit='s')
    """)

    # When
    result = testdir.runpytest()

    # Then
    assert result.ret == ExitCode.OK


def test_performance_slow(testdir):
    # Given
    testdir.makepyfile("""
        import pytest
        import time
        from pytest_performance import PerformanceException
        
        def foo():    
            time.sleep(2)
            return 1
            
        def test_sth(performance):
            with pytest.raises(PerformanceException):
                performance(foo)
    """)

    # When
    result = testdir.runpytest()

    # Then
    assert result.ret == ExitCode.OK


def test_performance_disable(testdir):
    # Given
    testdir.makepyfile("""
        import pytest
        import time
        from pytest_performance import PerformanceException

        def foo():    
            time.sleep(2)
            return 1

        def test_sth(performance):
            pass
    """)

    # When
    result = testdir.runpytest(SKIP_FLAG)

    # Then
    assert result.ret == ExitCode.OK


def test_performance_default(testdir):
    # Given
    testdir.makepyfile("""
        def test_sth():
            assert 1 == 1
    """)

    # When
    result = testdir.runpytest()

    # Then
    assert result.ret == ExitCode.OK
