INPUT_PATH = "./sample/lover/"

from typing import Any, Callable
from pathlib import Path
from importlib import import_module
import tomllib
from configparser import ConfigParser
from aseprite import Sprite
from PIL import Image

DIR = Path(__file__).resolve().parent.parent

input_path = DIR / INPUT_PATH
default_path = DIR / "./src/default/"

with open(input_path / "config.toml", "rb") as file:
    config = tomllib.load(file)
with open(default_path / "lover/config.toml", "rb") as file:
    default = tomllib.load(file)
    
def get_sprite(name) -> Path:
    for ext in ("aseprite", "ase"):
        path = Path(str(name) + "." + ext)
        if path.is_file():
            return path
    
    raise FileNotFoundError(f"No aseprite file found from '{name}'")

'''ase = {
    name: Sprite.open(get_sprite(input_path / name))
    for name in (
        "portrait",
        "xray",
        "mating_press",
        "reverse_cowgirl",
        "deepthroat",
        "ball_clench"
    )
}'''

global ini

def stringify(value) -> str:
    match value:
        case str():
            return f'"{value.replace('"', '\\"')}"'
        case bool():
            return "1" if value else "0"
        case _:
            return str(value)

def dig(obj, path: str):
    for i in path.split("."):
        obj = obj[i]
    return obj

def get(path: str):
    try:
        return dig(config, path)
    except KeyError:
        return dig(default, path)

def output_ini(key: str) -> None:
    output_path = (input_path / config["config"]["output_dir"][key]).resolve()
    output_path.mkdir(parents=True, exist_ok=True)
    with open(output_path / "custom_data.futa", "w") as output_file:
        ini.write(output_file)

#region -Vanilla

ini = ConfigParser(interpolation=None)

mapping: dict[str, dict[str, Any]] = \
    import_module("targets.wifes_bedroom.lover.config").to_config(get)
for section in mapping:
    ini[section] = {
        key: stringify(value) for (key, value) in mapping[section].items()
    }

output_ini("vanilla")

#region -Deeproom

ini = ConfigParser(interpolation=None)

mapping: dict[str, dict[str, Any]] = \
    import_module("targets.deeproom.lover.config").to_config(get)
for section in mapping:
    ini[section] = {
        key: stringify(value) for (key, value) in mapping[section].items()
    }

output_ini("Deeproom")
