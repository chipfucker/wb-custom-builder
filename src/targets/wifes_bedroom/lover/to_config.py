from typing import Any, Callable
from util import hex_to_rgb

def to_config(cfg: Callable[[str], Any]) -> dict[str, dict[str, Any]]:
    return {
        "info": {
            "name": cfg("meta.name"),
            "desc": cfg("meta.description"),
            "author": cfg("meta.author"),
        },
        "sprite": {
            "origin_x": cfg("body.origin.overall.x"),
            "origin_y": cfg("body.origin.overall.y"),
            "condom_y": cfg("body.condom.origin_y"),
            "standing_condom_y": cfg("body.condom.standing_offset_y"),
            "xray_x": cfg("xray.origin.x"),
            "xray_y": cfg("xray.origin.y"),
            "bulge_width": cfg("body.scale.bulge.width"),
            "bulge_height": cfg("body.scale.bulge.length"),
            "heavy_boobs": cfg("body.boobs.heavy"),
        },
        "portrait": {
            "origin_x": cfg("portrait.origin.x"),
            "origin_y": cfg("portrait.origin.y"),
            "head_offset": cfg("portrait.head_offset"),
            "nipple_x": cfg("portrait.nipples.position.x"),
            "nipple_y": cfg("portrait.nipples.position.y"),
            "nipple_size": cfg("portrait.nipples.size")
        },
        "stats": {
            "max_orgasms": cfg("stats.max_orgasms"),
            "max_pumps": cfg("stats.max_pumps"),
            "default_moans": not cfg("meta.custom_moans"),
            **{"cum_"+c: v for (c, v) in hex_to_rgb(cfg("colors.cum"))},
            **{"condom_"+c: v for (c, v) in hex_to_rgb(cfg("colors.condom"))},
            "lactate": cfg("body.boobs.lactating"),
            "flat": cfg("body.boobs.flat")
        }
    }
