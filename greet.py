"""Tiny sandbox module the factory uses to test its pipeline end to end."""


def greet(name: str) -> str:
    """Return a greeting for name."""
    return f"Hello, {name}!"


if __name__ == "__main__":
    import sys

    print(greet(sys.argv[1] if len(sys.argv) > 1 else "world"))
