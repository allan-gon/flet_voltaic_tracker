# built-ins
from winreg import OpenKey, HKEY_LOCAL_MACHINE, QueryValueEx
from platform import system
from os.path import abspath
from os import listdir
from json import load as json_load

# my code
from util.constants import (
    GAME_SUBFOLDER,
    KOVAAKS,
    DATA_FOLDER_PATH_FILE,
    STATS_SUBFOLDER,
)

# packages
from vdf import load


class SteamNotInRegistryError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.message = "Could not locate steam folder via Windows Registry"


class NonWindowsOSError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.message = "Auto finding Kovaaks data folder is only supported for Windows"


class KovaaksNotFoundError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.message = "Kovaaks not detected in any Steam folder"


class ManyKovaaksFolderFound(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.message = "Several Kovaaks folders found. Unclear which to use"


def find_steam_folders() -> list[str]:
    if system() == "Windows":
        try:
            bit_64 = "SOFTWARE\WOW6432Node\Valve\Steam"
            with OpenKey(HKEY_LOCAL_MACHINE, bit_64) as key:
                path = QueryValueEx(key, "InstallPath")[0]
        except FileNotFoundError:
            raise SteamNotInRegistryError

        with open(f"{path}/steamapps/libraryfolders.vdf", "r") as file:
            content = load(file)

        paths = []
        for key in content["libraryfolders"]:
            paths.append(content["libraryfolders"][key]["path"].replace("\\", "/"))
        # should return at least one path
        return paths
    else:
        raise NonWindowsOSError


def find_kovaaks_folder() -> str:
    steam_folders = find_steam_folders()
    kovaaks_paths = []

    for steam_folder in steam_folders:
        if KOVAAKS in listdir(f"{steam_folder}/{GAME_SUBFOLDER}"):
            kovaaks_paths.append(f"{steam_folder}/{GAME_SUBFOLDER}/{KOVAAKS}")

    if not kovaaks_paths:
        raise KovaaksNotFoundError
    elif len(kovaaks_paths) > 1:
        raise ManyKovaaksFolderFound
    else:
        return kovaaks_paths[0]


def parse(path: str) -> list[str]:
    # pretty sure score are always on the -24 line
    with open(path, "r") as file:
        score = file.readlines()[-24].split(",")[-1].strip()
    return score


def get_highscores(highscores: dict) -> None:
    with open(abspath(DATA_FOLDER_PATH_FILE), "r") as file:
        game_folder = file.read()
    full_dir = f"{game_folder}/{STATS_SUBFOLDER}"

    for fname in listdir(full_dir):
        # i think naive
        scenario = fname.split(" - Challenge - ")[0]
        if scenario in highscores:
            score = parse(f"{full_dir}/{fname}")
            try:
                score = float(score)
            except ValueError:
                with open(abspath("./logs/log"), "a") as file:
                    file.write(f"\n {fname}: {score}")
                continue
            if (highscores[scenario] == None) or (score > highscores[scenario]):
                highscores[scenario] = round(score, 2)


def select_color(layout: str, score: float, scenario: str) -> str:
    color = "white"
    with open(abspath(layout)) as file:
        schema = json_load(file)
    for scen_type in schema["types"]:
        for sub_type in scen_type["subtypes"]:
            for scen in sub_type["scenarios"]:
                if scen["name"] == scenario:
                    for idx in range(1, len(scen["scores"]) + 1):
                        if score >= scen["scores"][-idx]:
                            color = schema["ranks"][-idx]["other_color"]
                            break

    return color
