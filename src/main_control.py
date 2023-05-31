# built-ins
from os import listdir

# my code
from src.table import VoltStyleTable
from src.settings_view import SettingsView
from util.constants import VOLT_S4_EASY

# packages
from flet import (
    Container,
    Column,
    Row,
    alignment,
    Dropdown,
    dropdown,
    IconButton,
    icons,
    ControlEvent,
)


def add_settings_view(event: ControlEvent) -> None:
    event.page.views.append(SettingsView(page=event.page))
    event.page.update()


def change_table(event: ControlEvent) -> None:
    event.page.controls[0].controls.pop()
    event.page.controls[0].controls.append(
        VoltStyleTable(f"./layouts/{event.control.value}", expand=9)
    )
    event.page.update()


def refresh(event: ControlEvent) -> None:
    layout = event.page.controls[0].controls[-1].layout
    event.page.controls[0].controls.pop()
    event.page.controls[0].controls.append(VoltStyleTable(layout, expand=9))
    event.page.update()


class MainControl(Column):
    def __init__(self):
        super().__init__()
        self.expand = True

    def _build(self):
        self.controls = [
            Row(
                expand=1,
                controls=[
                    Column(
                        controls=[
                            Row(
                                controls=[
                                    Dropdown(
                                        options=[
                                            dropdown.Option(key=file)
                                            for file in listdir("./layouts")
                                        ],
                                        on_change=change_table,
                                    ),
                                    IconButton(icon=icons.REFRESH, on_click=refresh),
                                ]
                            )
                        ]
                    ),
                    Container(
                        expand=True,
                        content=IconButton(
                            icon=icons.SETTINGS,
                            on_click=add_settings_view,
                        ),
                        alignment=alignment.top_right,
                    ),
                ],
            ),
            VoltStyleTable(VOLT_S4_EASY, expand=9),
        ]
