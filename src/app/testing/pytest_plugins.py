import pytest
import httpretty


def pytest_runtest_setup(item: pytest.Item) -> None:
    if len(list(item.iter_markers("httpretty"))) > 0:
        httpretty.reset()
        httpretty.enable(allow_net_connect=False)


def pytest_runtest_teardown(item: pytest.Item, nextitem: pytest.Item) -> None:
    if len(list(item.iter_markers("httpretty"))) > 0:
        httpretty.disable()
        httpretty.reset()
