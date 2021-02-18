import pytest
from textwrap import dedent


@pytest.fixture()
def file_structure(pytester):
    """
    test_foo.py
    test_bar.py
    sub/foo.py
    sub2/bar.py
    """
    content = dedent(
        """
    from foo import foo

    def test_foo():
        assert foo() == 1
    """
    )
    pytester.makepyfile(test_foo=content)

    content = dedent(
        """
    from bar import bar

    def test_bar():
        assert bar() == 2
    """
    )
    pytester.makepyfile(test_bar=content)

    content = dedent(
        """
    def foo():
        return 1
    """
    )
    foo_py = pytester.mkdir("sub") / "foo.py"
    foo_py.write_text(content, encoding="utf-8")

    content = dedent(
        """
    def bar():
        return 2
    """
    )
    bar_py = pytester.mkdir("sub2") / "bar.py"
    bar_py.write_text(content, encoding="utf-8")


def test_one_dir(pytester, file_structure):
    pytester.makefile(".ini", pytest="[pytest]\nsrcpaths=sub\n")
    result = pytester.runpytest("test_foo.py")
    result.assert_outcomes(passed=1)


def test_two_dirs(pytester, file_structure):
    pytester.makefile(".ini", pytest="[pytest]\nsrcpaths=sub sub2\n")
    result = pytester.runpytest("test_foo.py", "test_bar.py")
    result.assert_outcomes(passed=2)


def test_module_not_found(pytester, file_structure):
    pytester.makefile(".ini", pytest="[pytest]\n")  # no srcpaths listed
    result = pytester.runpytest("test_foo.py")
    result.assert_outcomes(errors=1)
    expected_error = "E   ModuleNotFoundError: No module named 'foo'"
    result.stdout.fnmatch_lines([expected_error])


def test_no_ini(pytester, file_structure):
    result = pytester.runpytest("test_foo.py")
    result.assert_outcomes(errors=1)
    expected_error = "E   ModuleNotFoundError: No module named 'foo'"
    result.stdout.fnmatch_lines([expected_error])

