from typing import Any

def to_config(cfg) -> dict[str, dict[str, Any]]:
    return {
        "info": {
            "name": cfg("meta.name"),
            "desc": cfg("meta.description"),
            "author": cfg("meta.author"),
        },
        "sprite": {},
        "portrait": {},
        "stats": {}
    }