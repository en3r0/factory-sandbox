"""Tiny sandbox module the factory uses to test its pipeline end to end."""


def greet(name: str, shout: bool = False) -> str:
    """Return a greeting for name; uppercases it when shout is True."""
    greeting = f"Hello, {name}!"
    return greeting.upper() if shout else greeting


if __name__ == "__main__":
    import sys

    print(greet(sys.argv[1] if len(sys.argv) > 1 else "world"))
