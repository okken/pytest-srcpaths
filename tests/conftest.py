import pytest
from textwrap import dedent
from _pytest.pytester import Pytester

pytest_plugins = "pytester"



@pytest.fixture()
def file_structure(pytester: Pytester) -> None:
    pytester.makepyfile(
        test_foo="""
        from foo import foo

        def test_foo():
            assert foo() == 1
        """
    )

    pytester.makepyfile(
        test_bar="""
        from bar import bar

        def test_bar():
            assert bar() == 2
        """
    )

    foo_py = pytester.mkdir("sub") / "foo.py"
    content = dedent(
        """
        def foo():
            return 1
        """
    )
    foo_py.write_text(content, encoding="utf-8")

    bar_py = pytester.mkdir("sub2") / "bar.py"
    content = dedent(
        """
        def bar():
            return 2
        """
    )
    bar_py.write_text(content, encoding="utf-8")

