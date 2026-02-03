"""Tests for example module."""

from magic_umbrella import example


def test_hello_default():
    """Test hello with default argument."""
    assert example.hello() == "Hello, World!"


def test_hello_with_name():
    """Test hello with custom name."""
    assert example.hello("Python") == "Hello, Python!"
