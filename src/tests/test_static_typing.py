from typing import TypeVar

import pytest

from pyodide.ffi import JsDoubleProxy, JsPromise, create_once_callable, create_proxy


@pytest.mark.mypy_testing
def test_create_proxy():
    _: int = create_proxy(42).unwrap()


@pytest.mark.mypy_testing
def test_generic():
    async def _(a: JsPromise[int]) -> str:
        return await a.then(str)  # type:ignore[misc]

    def _(b: JsDoubleProxy[str]) -> str:
        return b.unwrap()


@pytest.mark.mypy_testing
def test_callable_generic():
    T = TypeVar("T", int, float, str)

    def f(x: T) -> T:
        return x * 2

    _: tuple[int, str] = create_once_callable(f)(2), create_proxy(f)("")


@pytest.mark.mypy_testing
def test_decorator_usage():
    T = TypeVar("T")

    @create_once_callable
    def f(x: T) -> list[T]:
        return [x]

    _: list[tuple[int, str]] = f((int("1"), str(1)))
