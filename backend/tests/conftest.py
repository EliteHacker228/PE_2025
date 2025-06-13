# tests/conftest.py
import pytest

def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "load: mark test as load test"
    )