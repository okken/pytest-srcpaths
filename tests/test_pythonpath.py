import sys
from typing import Generator
from typing import List
from typing import Optional

import pytest
from _pytest.pytester import Pytester


def test_one_dir_pythonpath(pytester: Pytester, file_structure) -> None:
    pytester.makefile(".ini", pytest="[pytest]\npythonpath=sub\n")
    result = pytester.runpytest("test_foo.py")
    assert result.ret == 0
    result.assert_outcomes(passed=1)


def test_two_dirs_pythonpath(pytester: Pytester, file_structure) -> None:
    pytester.makefile(".ini", pytest="[pytest]\npythonpath=sub sub2\n")
    result = pytester.runpytest("test_foo.py", "test_bar.py")
    assert result.ret == 0
    result.assert_outcomes(passed=2)


def test_unconfigure_unadded_dir_pythonpath(pytester: Pytester) -> None:
    pytester.makeconftest(
        """
        def pytest_configure(config):
          config.addinivalue_line("pythonpath", "sub")
        """
    )
    pytester.makepyfile(
        """
        import sys

        def test_something():
            pass
        """
    )
    result = pytester.runpytest()
    result.assert_outcomes(passed=1)


def test_clean_up_pythonpath(pytester: Pytester) -> None:
    """Test that the srcpaths plugin cleans up after itself."""
    pytester.makefile(".ini", pytest="[pytest]\npythonpath=I_SHALL_BE_REMOVED\n")
    pytester.makepyfile(test_foo="""def test_foo(): pass""")

    before: Optional[List[str]] = None
    after: Optional[List[str]] = None

    class Plugin:
        @pytest.hookimpl(hookwrapper=True, tryfirst=True)
        def pytest_unconfigure(self) -> Generator[None, None, None]:
            nonlocal before, after
            before = sys.path.copy()
            yield
            after = sys.path.copy()

    result = pytester.runpytest_inprocess(plugins=[Plugin()])
    assert result.ret == 0

    assert before is not None
    assert after is not None
    assert any("I_SHALL_BE_REMOVED" in entry for entry in before)
    assert not any("I_SHALL_BE_REMOVED" in entry for entry in after)
