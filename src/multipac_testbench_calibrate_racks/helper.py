"""Define general-use functions."""


def printc(message: str, color="red") -> None:
    """Print colored message."""
    normal_code = "\x1b[0m"
    escape_code = normal_code
    if color in ("red", "r"):
        escape_code = "\x1b[31m"
    if color in ("blue", "b"):
        escape_code = "\x1b[34m"
    if color in ("green", "g"):
        escape_code = "\x1b[32m"
    if color in ("magenta", "m"):
        escape_code = "\x1b[35m"
    if color in ("cyan", "c"):
        escape_code = "\x1b[36m"
    print(f"{escape_code}{message}{normal_code}")
