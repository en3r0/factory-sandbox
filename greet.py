"""Tiny sandbox module the factory uses to test its pipeline end to end."""


def greet(name: str, shout: bool = False) -> str:
    """Return a greeting for name; uppercases it when shout is True."""
    greeting = f"Hello, {name}!"
    return greeting.upper() if shout else greeting


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Print a greeting.")
    parser.add_argument("name", nargs="?", default="world", help="the name to greet")
    parser.add_argument("--shout", action="store_true", help="print the greeting in uppercase")
    args = parser.parse_args()
    print(greet(args.name, shout=args.shout))
