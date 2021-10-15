# pytest-srcpaths

Add paths to `sys.path`.  
A pytest plugin to help pytest find the code you want to test.


## Installation

Install with pip:

    pip install pytest-srcpaths


## Usage

Add a line in your pytest.ini file with a key of `srcpaths`.
It should contain a space-separated list of paths.

    [pytest]
    srcpaths = src lib

Paths are relative to the directory that pytest.ini is in.  
You can include the top level directory with a dot.

    [pytest]
    srcpaths = .

## Alternatively, use `pythonpath`

The option `pythonpath` also works the same.

    [pytest]
    pythonpath = src lib

pytest 7 (not released yet) is planned to include the `pythonpath` option. 

For pytest 6.2.x, this plugin will work.


## Changelog

* 1.2.1 - Add `pythonpath` as an alternative to `srcpath` option for pytest versions < 7.0.0
  * this is to allow this project to act as a temporary workaround until pytest 7 is released

## Similar project

This plugin was inspired by [pytest-pythonpath](https://pypi.org/project/pytest-pythonpath/) whose implementation and scope are a bit different.
