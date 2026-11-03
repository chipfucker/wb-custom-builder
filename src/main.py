INPUT_PATH = "./sample/lover/"

from pathlib import Path
import tomllib
from configparser import ConfigParser
# from aseprite import Sprite

type TomlValue = str | bool | int | float
type Toml = dict[str, TomlValue | Toml | list]

EXPECTED_FILENAME = "config.toml"

DIR = Path(__file__).resolve().parent.parent

input_path = DIR / INPUT_PATH
default_path = DIR / "./src/default/"

def stringify(value: str | bool | int | float) -> str:  
  match value:
    case str():
      return f'"{value.replace('"', '\\"')}"'
    case bool():
      return "1" if value else "0"
    case _:
      return str(value)

def get(*path: str) -> str:
  if len(path) == 0:
    return "TEMP"
    
  for obj in (config, default):
    for key in path:
      try:
        obj = obj[key]
      except KeyError:
        break
    else:
      return stringify(obj)
  
  raise KeyError(path)
  

# --- Vanilla ---

with open(input_path / EXPECTED_FILENAME, "rb") as file:
  config = tomllib.load(file)
with open(default_path / "lover/config.toml", "rb") as file:
  default = tomllib.load(file)

ini = ConfigParser(interpolation=None)

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
  "xray_x": get(),
  "xray_y": get(),
  "bulge_width": get("body", "scale", "bulge", "width"),
  "bulge_height": get("body", "scale", "bulge", "length"),
  "heavy_boobs": get("body", "boobs", "heavy"),
}
ini["portrait"] = {
  "origin_x": get(),
  "origin_y": get(),
  "head_offset": get(),
  "nipple_x": get(),
  "nipple_y": get(),
  "nipple_size": get()
}
ini["stats"] = {
  "max_orgasms": get(),
  "max_pumps": get(),
  "default_moans": not get("meta", "custom_moans"),
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
