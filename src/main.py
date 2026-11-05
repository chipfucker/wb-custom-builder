INPUT_PATH = "./sample/lover/"

from pathlib import Path
import tomllib
from configparser import ConfigParser
from aseprite import Sprite
from pillow import Image

DIR = Path(__file__).resolve().parent.parent
FILENAME_SEPARATOR = "_"

def filename(name: str) -> str:
  return FILENAME_SEPARATOR.join(name.split(" "))

input_path = DIR / INPUT_PATH
default_path = DIR / "./src/default/"

with open(input_path / "config.toml", "rb") as file:
  config = tomllib.load(file)
with open(default_path / "lover/config.toml", "rb") as file:
  default = tomllib.load(file)

global ini: ConfigParser
global ase

def stringify(value) -> str:
  match value:
    case str():
      return f'"{value.replace('"', '\\"')}"'
    case bool():
      return "1" if value else "0"
    case _:
      return str(value)

def dig(obj, path: tuple[str | int, ...]):
  for i in path:
    obj = obj[i]
  return stringify(obj)

def get(*path: *tuple[str, *tuple[str | int, ...]]) -> str:
  try:
    return dig(config, path)
  except KeyError:
    return dig(default, path)

def output_ini(key: str) -> None:
  output_path = (input_path / config["config"]["output_dir"][key]
                ).resolve()
  output_path.mkdir(parents=True, exist_ok=True)
  with open(output_path / "custom_data.futa", "w") as output_file:
    ini.write(output_file)

#region ---Vanilla---

ini = ConfigParser(interpolation=None)

cum_color = config["colors"]["cum"].lstrip("#")
condom_color = config["colors"]["condom"].lstrip("#")
cum_r, cum_g, cum_b = tuple(
  str(int(cum_color[i:i+2], 16)) for i in (0, 2, 4)
)
condom_r, condom_g, condom_b = tuple(
  str(int(condom_color[i:i+2], 16)) for i in (0, 2, 4)
)

ini["info"] = {
  "name": get("meta", "name"),
  "desc": get("meta", "description"),
  "author": get("meta", "author")
}
ini["sprite"] = {
  "origin_x": get("body", "origin", "overall", "x"),
  "origin_y": get("body", "origin", "overall", "y"),
  "condom_y": get("body", "condom", "origin_y"),
  "standing_condom_y": get("body", "condom", "standing_offset_y"),
  "xray_x": get("xray", "origin", "x"),
  "xray_y": get("xray", "origin", "y"),
  "bulge_width": get("body", "scale", "bulge", "width"),
  "bulge_height": get("body", "scale", "bulge", "length"),
  "heavy_boobs": get("body", "boobs", "heavy"),
}
ini["portrait"] = {
  "origin_x": get("portrait", "origin", "x"),
  "origin_y": get("portrait", "origin", "y"),
  "head_offset": get("portrait", "head_offset"),
  "nipple_x": get("portrait", "nipples", "position", "x"),
  "nipple_y": get("portrait", "nipples", "position", "y"),
  "nipple_size": get("portrait", "nipples", "size")
}
ini["stats"] = {
  "max_orgasms": get("stats", "max_orgasms"),
  "max_pumps": get("stats", "max_pumps"),
  "default_moans": "0" if config["meta"]["custom_moans"] else "1",
  "cum_r": cum_r,
  "cum_g": cum_g,
  "cum_b": cum_b,
  "condom_r": condom_r,
  "condom_g": condom_g,
  "condom_b": condom_b,
  "lactate": get("body", "boobs", "lactating"),
  "flat": get("body", "boobs", "flat")
}

output_ini("vanilla")

ase = {
  key: Sprite.open(input_path / filename(name + ".aseprite"))
  for key, name in {
    "portrait": "portrait",
    "xray": "xray",
    "mating_press": "mating press",
    "reverse_cowgirl": "reverse cowgirl",
    "deepthroat": "deepthroat",
    "ball_clench": "ball clench"
  }.items()
}

#region ---Deeproom---

ini = ConfigParser(interpolation=None)

ini["sprite"] = {
  "origin_x": get("body", "origin", "overall", "x"),
  "origin_y": get("body", "origin", "overall", "y"),
  "cowgirl_origin_x": get("body", "origin", "cowgirl", "x"),
  "cowgirl_origin_y": get("body", "origin", "cowgirl", "y")
}
ini["portrait"] = {
  "origin_x": get("portrait", "origin", "x"),
  "origin_y": get("portrait", "origin", "y")
}
ini["condom"] = {
  "condom_y_mpress": get("body", "condom", "mating_press_offset_y"),
  "condom_y_cowgirls": get("body", "condom", "cowgirl_offset_y")
}
ini["stats"] = {
  "max_orgasms": get("stats", "max_orgasms"),
  "top_boob_size": get("body", "scale", "boobs"),
  "top_ass_size": get("body", "scale", "ass"),
  "top_penis_length": get("body", "scale", "penis", "length"),
  "top_penis_width": get("body", "scale", "penis", "width"),
  "ball_size": get("body", "scale", "balls"),
  "virility_modifier": get("stats", "virility"),
  "cum_volume_modifier": get("stats", "cum_volume"),
  "stroke_depth": get("stats", "thrust_strength"),
  "stroke_speed": get("stats", "thrust_speed"),
  "pump_delay": str(config["stats"]["pump_delay"] * 60)
}
ini["penis"] = {
  "penis_type_index": str(sum(
    i for (k, i) in (("knotted", 1), ("equine", 2))
      if config["body"]["penis"][k]
  ))
}
PILLS = (
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
)
ini["pills"] = {i+"_pill": get("pills", i) for i in PILLS}

output_ini("Deeproom")
