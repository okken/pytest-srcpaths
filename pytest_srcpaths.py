"""
Add paths to sys.path
"""
import sys

__version__ = "1.0.0"

def pytest_addoption(parser):
    parser.addini("srcpaths",
                  type="pathlist",
                  help="Add paths to sys.path")


def pytest_configure(config):
    paths_from_ini = config.getini("srcpaths")
    if paths_from_ini:
        for path in paths_from_ini:
            sys.path.insert(0, str(path))



