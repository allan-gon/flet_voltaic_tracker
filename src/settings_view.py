# built-in
from os.path import abspath

# my code
from util.constants import DATA_FOLDER_PATH_FILE

# packages
from flet import (
    View,
    FilePickerResultEvent,
    ElevatedButton,
    Text,
    Row,
    alignment,
    AppBar,
    IconButton,
    icons,
    FontWeight,
    ControlEvent,
    Page,
)


def go_back(event: ControlEvent) -> None:
    # TODO: refresh, will yoink from refresh button
    event.page.views.pop()
    event.page.update()


def change_displayed_folder(result: FilePickerResultEvent) -> None:
    # save to file in case it's at some strange location
    with open(abspath(DATA_FOLDER_PATH_FILE), "w") as file:
        file.write(result.path)
    # reflect change in widget
    result.page.views[-1].controls[-1].controls[0].value = result.path
    result.page.update()


class SettingsView(View):
    def __init__(self, page: Page):
        super().__init__()
        with open(DATA_FOLDER_PATH_FILE, "r") as file:
            content = file.read()
        if content:
            self.path = content
        else:
            self.path = "None"
        self.page = page

    def _build(self):
        self.expand = True
        self.route = "/settings"
        self.appbar = AppBar(
            leading=IconButton(icon=icons.ARROW_BACK, on_click=go_back)
        )
        self.controls = [
            Text(value="Reading from:", weight=FontWeight.BOLD),
            Row(
                alignment=alignment.center,
                controls=[
                    Text(value=self.path),
                    ElevatedButton(
                        text="Select another folder",
                        on_click=self.page.overlay[0].get_directory_path,
                    ),
                ],
            ),
        ]
