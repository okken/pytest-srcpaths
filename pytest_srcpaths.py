"""
Add paths to sys.path
"""
import sys

import pytest

__version__ = "1.1.0"

def pytest_addoption(parser) -> None:
    parser.addini("srcpaths",
                  type="pathlist",
                  help="Add paths to sys.path",
                  default=[])


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config) -> None:
    # `pythonpath = a b` will set `sys.path` to `[a, b, x, y, z, ...]`
    for path in reversed(config.getini("srcpaths")):
        sys.path.insert(0, str(path))


@pytest.hookimpl(trylast=True)
def pytest_unconfigure(config) -> None:
    for path in config.getini("srcpaths"):
        path_str = str(path)
        if path_str in sys.path:
            sys.path.remove(path_str)



