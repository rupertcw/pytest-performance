==================
pytest-performance
==================

.. image:: https://img.shields.io/pypi/v/pytest-performance.svg
    :target: https://pypi.org/project/pytest-performance
    :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/pytest-performance.svg
    :target: https://pypi.org/project/pytest-performance
    :alt: Python versions

.. image:: https://travis-ci.org/rupertcw/pytest-performance.svg?branch=master
    :target: https://travis-ci.org/rupertcw/pytest-performance
    :alt: See Build Status on Travis CI

.. image:: https://ci.appveyor.com/api/projects/status/github/rupertcw/pytest-performance?branch=master
    :target: https://ci.appveyor.com/project/rupertcw/pytest-performance/branch/master
    :alt: See Build Status on AppVeyor

A simple plugin to ensure the execution of critical sections of code has not been impacted between releases.

----


Features
--------

* Parameterisation of profiling parameters
* Support for all time measurement units


Requirements
------------

* pint == 0.15


Installation
------------

You can install "pytest-performance" via `pip`_ from `PyPI`_::

    $ pip install pytest-performance


Usage
-----

* Default

.. code-block:: python

    def my_func(*args, **kwargs):
        return 123

    def test_my_func(performance):
        # Check my_func runs within 1 second for 10000 iterations.
        result = performance(my_func)
        assert result == 123

* Set custom time amount

.. code-block:: python

    def my_func(*args, **kwargs):
        return 123

    def test_my_func(performance):
        # Check my_func runs within 10 seconds for 10000 iterations.
        result = performance(my_func, target=10)
        assert result == 123

* Set custom time amount and unit (pint units supported)

.. code-block:: python

    def my_func(*args, **kwargs):
        return 123

    def test_my_func(performance):
        # Check my_func runs within 1 nanosecond for 10000 iterations.
        result = performance(my_func, target=10, unit='ns')
        assert result == 123

* Set custom time amount, unit and number of iterations

.. code-block:: python

    def my_func(*args, **kwargs):
        return 123

    def test_my_func(performance):
        # Check my_func runs within 1 nanosecond for 10 iterations.
        result = performance(my_func, target=10, unit='ns', iterations=10)
        assert result == 123

* Fixture can be disabled by passing '--performance-skip' to pytest

Contributing
------------
Contributions are very welcome. Tests can be run with `tox`_, please ensure
the coverage at least stays the same before you submit a pull request.

License
-------

Distributed under the terms of the `MIT`_ license, "pytest-performance" is free and open source software


Issues
------

If you encounter any problems, please `file an issue`_ along with a detailed description.

.. _`Cookiecutter`: https://github.com/audreyr/cookiecutter
.. _`@hackebrot`: https://github.com/hackebrot
.. _`MIT`: http://opensource.org/licenses/MIT
.. _`GNU GPL v3.0`: http://www.gnu.org/licenses/gpl-3.0.txt
.. _`Apache Software License 2.0`: http://www.apache.org/licenses/LICENSE-2.0
.. _`cookiecutter-pytest-plugin`: https://github.com/pytest-dev/cookiecutter-pytest-plugin
.. _`file an issue`: https://github.com/rupertcw/pytest-performance/issues
.. _`pytest`: https://github.com/pytest-dev/pytest
.. _`tox`: https://tox.readthedocs.io/en/latest/
.. _`pip`: https://pypi.org/project/pip/
.. _`PyPI`: https://pypi.org/project
