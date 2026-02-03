"""Example module."""


def hello(name: str = "World") -> str:
    """Return a greeting message.

    Args:
        name: Name to greet

    Returns:
        Greeting message
    """
    return f"Hello, {name}!"
