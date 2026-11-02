from pathlib import Path, PurePath
import tomllib
from configparser import ConfigParser
from aseprite import Sprite

INPUT_PATH = "./sample/lover/"

EXPECTED_FILENAME = "config.toml"

input_path = PurePath(INPUT_PATH)

with open(input_path / EXPECTED_FILENAME, "rb") as file:
  toml = tomllib.load(file)

vanilla_ini = ConfigParser(interpolation=None)
deeproom_ini = ConfigParser(interpolation=None)

def default(value: str | bool | int | float | None, default: str) -> str:
  if value is None:
    return default
  
  match value:
    case str(): return value
    case bool(): return "1" if value else "0"
    case int() | float(): return str(value)

vanilla_ini["info"] = {
  "name": default(toml["meta"]["name"], "Example"),
  "desc": default(toml["meta"]["description"], "A template you may use to create your own custom lover!"),
  "author": default(toml["meta"]["author"], "Aplove")
}
vanilla_ini["sprite"] = {
  "origin_x": default(toml["body"]["origin"]["overall"]["x"], "80"),
  "origin_y": default(toml["body"]["origin"]["overall"]["y"], "84"),
  "condom_y": default(toml["body"]["condom"]["origin_y"], "78")
}
# more keys to come...

output_path = input_path / EXPECTED_FILENAME / toml["config"]["output_dir"]["vanilla"]
Path(output_path).mkdir(parents=True, exist_ok=True)
with open(output_path / "custom_data.futa", "w") as output_file:
  vanilla_ini.write(output_file)
