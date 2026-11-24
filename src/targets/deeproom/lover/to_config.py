from typing import Any, Callable

def to_config(cfg: Callable[[str], Any]) -> dict[str, dict[str, Any]]:
    return {
        "sprite": {
            "origin_x": cfg("body.origin.overall.x"),
            "origin_y": cfg("body.origin.overall.y"),
            "cowgirl_origin_x": cfg("body.origin.cowgirl.x"),
            "cowgirl_origin_y": cfg("body.origin.cowgirl.y")
        },
        "portrait": {
            "origin_x": cfg("portrait.origin.x"),
            "origin_y": cfg("portrait.origin.y")
        },
        "condom": {
            "condom_y_mpress": cfg("body.condom.mating_press_offset_y"),
            "condom_y_cowgirls": cfg("body.condom.cowgirl_offset_y")
        },
        "stats": {
            "max_orgasms": cfg("stats.max_orgasms"),
            "top_boob_size": cfg("body.scale.boobs"),
            "top_ass_size": cfg("body.scale.ass"),
            "top_penis_length": cfg("body.scale.penis.length"),
            "top_penis_width": cfg("body.scale.penis.width"),
            "ball_size": cfg("body.scale.balls"),
            "virility_modifier": cfg("stats.virility"),
            "cum_volume_modifier": cfg("stats.cum_volume"),
            "stroke_depth": cfg("stats.thrust_strength"),
            "stroke_speed": cfg("stats.thrust_speed"),
            "pump_delay": cfg("stats.pump_delay") * 60
        },
        "penis": {
            "penis_type_index": sum(
                i for (k, i) in (("knotted", 1), ("equine", 2))
                  if cfg("body.penis."+k)
            )
        },
        "pills": {i+"_pill": cfg("pills."+i) for i in (
            "contraceptive",
            "mega_sperm",
            "equine",
            "knotted",
            "extra_thick",
            "diphallia",
            "ovulation",
            "stamina",
            "leaky",
            "hyper_breeding"
        )},
    }
