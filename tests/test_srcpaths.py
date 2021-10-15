import sys
from typing import Generator
from typing import List
from typing import Optional

import pytest
from _pytest.pytester import Pytester



def test_one_dir(pytester: Pytester, file_structure) -> None:
    pytester.makefile(".ini", pytest="[pytest]\nsrcpaths=sub\n")
    result = pytester.runpytest("test_foo.py")
    assert result.ret == 0
    result.assert_outcomes(passed=1)


def test_two_dirs(pytester: Pytester, file_structure) -> None:
    pytester.makefile(".ini", pytest="[pytest]\nsrcpaths=sub sub2\n")
    result = pytester.runpytest("test_foo.py", "test_bar.py")
    assert result.ret == 0
    result.assert_outcomes(passed=2)


def test_module_not_found(pytester: Pytester, file_structure) -> None:
    """Without the srcpaths setting, the module should not be found."""
    pytester.makefile(".ini", pytest="[pytest]\n")
    result = pytester.runpytest("test_foo.py")
    assert result.ret == pytest.ExitCode.INTERRUPTED
    result.assert_outcomes(errors=1)
    expected_error = "E   ModuleNotFoundError: No module named 'foo'"
    result.stdout.fnmatch_lines([expected_error])


def test_no_ini(pytester: Pytester, file_structure) -> None:
    """If no ini file, test should error."""
    result = pytester.runpytest("test_foo.py")
    assert result.ret == pytest.ExitCode.INTERRUPTED
    result.assert_outcomes(errors=1)
    expected_error = "E   ModuleNotFoundError: No module named 'foo'"
    result.stdout.fnmatch_lines([expected_error])


def test_unconfigure_unadded_dir(pytester: Pytester) -> None:
    """
    The srcpaths handling adds paths during pytest_load_initial_conftests.
    This test adds the ini pythopath setting after that, during pytest_configure.
    Really, any time before unconfigure, would work.
    Then, when pytest_unconfigure happens, it tries to remove the sub from sys.path,
    but it isn't there.

    Therefore, the point of this test is to make sure that behavior works, that unconfigure
    doesn't blow up if a directory isn't in sys.path before unconfigure.
    """
    pytester.makeconftest(
        """
        def pytest_configure(config):
          config.addinivalue_line("srcpaths", "sub")
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


def test_clean_up(pytester: Pytester) -> None:
    """Test that the srcpaths plugin cleans up after itself."""
    # This is tough to test behaviorly because the cleanup really runs last.
    # So the test make several implementation assumptions:
    # - Cleanup is done in pytest_unconfigure().
    # - Not a hookwrapper.
    # So we can add a hookwrapper ourselves to test what it does.
    pytester.makefile(".ini", pytest="[pytest]\nsrcpaths=I_SHALL_BE_REMOVED\n")
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


