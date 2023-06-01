# built-in
from os.path import abspath

# packages
from flet import app, Page, FilePicker, SnackBar, Text

# my code
from src.main_control import MainControl
from util.constants import DATA_FOLDER_PATH_FILE
from src.settings_view import change_displayed_folder, SettingsView
from util.helper import (
    find_kovaaks_folder,
    SteamNotInRegistryError,
    NonWindowsOSError,
    KovaaksNotFoundError,
    ManyKovaaksFolderFound,
)


def main(page: Page) -> None:
    page.window_height = 600
    page.window_width = 800
    page.overlay.append(FilePicker(on_result=change_displayed_folder))

    # load folder from file
    with open(abspath(DATA_FOLDER_PATH_FILE), "r") as file:
        content = file.read().strip()
    # if something saved
    if content:
        page.add(MainControl())
    else:
        # otherwise try and find it
        try:
            game_folder = find_kovaaks_folder()
        # if you can't
        except (
            SteamNotInRegistryError,
            NonWindowsOSError,
            KovaaksNotFoundError,
            ManyKovaaksFolderFound,
        ) as e:
            page.add(MainControl())
            # let the user set it
            page.views.append(SettingsView(page=page))
            # show an error
            page.show_snack_bar(
                snack_bar=SnackBar(
                    content=Text(
                        value=e.message + "\nManually select your kovaaks folder",
                        color="white",
                    ),
                    open=True,
                    bgcolor="#FF3030",
                )
            )
        # if you did find it
        else:
            # save and show
            with open(DATA_FOLDER_PATH_FILE, "w") as file:
                file.write(game_folder)
            page.add(MainControl())

    page.update()


if __name__ == "__main__":
    app(target=main)
