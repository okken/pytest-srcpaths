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

## Similar project

This plugin was inspired by [pytest-pythonpath](https://pypi.org/project/pytest-pythonpath/) whose implementation and scope are a bit different.
