"""
Add paths to sys.path
"""
from packaging import version
import sys

import pytest

__version__ = "1.2.1"

def pytest_addoption(parser) -> None:
    parser.addini("srcpaths",
                  type="pathlist",
                  help="Add paths to sys.path",
                  default=[])
    if version.parse(pytest.__version__) < version.parse("7.0.0"):
        parser.addini("pythonpath",
                      type="pathlist",
                      help="Add paths to sys.path",
                      default=[])


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config) -> None:
    # `srcpaths = a b` will set `sys.path` to `[a, b, x, y, z, ...]`
    for path in reversed(config.getini("srcpaths")):
        sys.path.insert(0, str(path))
    if version.parse(pytest.__version__) < version.parse("7.0.0"):
        for path in reversed(config.getini("pythonpath")):
            sys.path.insert(0, str(path))


@pytest.hookimpl(trylast=True)
def pytest_unconfigure(config) -> None:
    for path in config.getini("srcpaths"):
        path_str = str(path)
        if path_str in sys.path:
            sys.path.remove(path_str)
    if version.parse(pytest.__version__) < version.parse("7.0.0"):
        for path in config.getini("pythonpath"):
            path_str = str(path)
            if path_str in sys.path:
                sys.path.remove(path_str)



