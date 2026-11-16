def hex_to_rgb(string: str) -> tuple[tuple[str, int], ...]:
    string = string.lstrip("#")
    r, g, b = (int(string[i:i+2], 16) for i in (0, 2, 4))
    return tuple(zip(("r", "g", "b"), (r, g, b)))
