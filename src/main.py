INPUT_PATH = "./sample/lover/"

import re as regex
from pathlib import Path
import tomllib
from configparser import ConfigParser
# from aseprite import Sprite

EXPECTED_FILENAME = "config.toml"

DIR = Path(__file__).resolve().parent.parent

input_path = DIR / INPUT_PATH
default_path = DIR / "./src/default/"

def stringify(value) -> str:  
  match value:
    case str():
      return f'"{value.replace('"', '\\"')}"'
    case bool():
      return "1" if value else "0"
    case int() | float():
      return str(value)
    case _:
      return str(value)

def get(*path: str | int) -> str:
  error = None

  for obj in (config, default):
    for key in path:
      try:
        obj = obj[key]  # type: ignore
      except KeyError as e:
        error = e
        break
    else:
      return stringify(obj)  # type: ignore
    
  raise error
  

# --- Vanilla ---

with open(input_path / EXPECTED_FILENAME, "rb") as file:
  config = tomllib.load(file)
with open(default_path / "lover/config.toml", "rb") as file:
  default = tomllib.load(file)

ini = ConfigParser(interpolation=None)

try:
  cum_color = int(config["colors"]["cum"][1:7], 16)
  condom_color = int(config["colors"]["cum"][1:7], 16)
except ValueError as error:
  hex = regex.search(r"(?<=').*(?='$)", [*error.args][0]).string  # type: ignore
  print(f"Invalid color ({hex})")
  quit()
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
  "max_orgasms": get(),
  "max_pumps": get(),
  "default_moans": "0" if get("meta", "custom_moans") else "1",
  "cum_r": get(),
  "cum_g": get(),
  "cum_b": get(),
  "condom_r": get(),
  "condom_g": get(),
  "condom_b": get(),
  "lactate": get("body", "boobs", "lactating"),
  "flat": get("body", "boobs", "flat")
}

output_path = (input_path / EXPECTED_FILENAME
               / config["config"]["output_dir"]["vanilla"]
              ).resolve()
output_path.mkdir(parents=True, exist_ok=True)
with open(output_path / "custom_data.futa", "w") as output_file:
  ini.write(output_file)
