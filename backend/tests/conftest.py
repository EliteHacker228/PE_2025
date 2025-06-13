import pytest  # noqa: F401


def pytest_configure(config):
    config.addinivalue_line("markers", "load: mark test as load test")
