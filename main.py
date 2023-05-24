# packages
from flet import app, Page, Row, FloatingActionButton, icons, ControlEvent

# my code
from src.table import VoltStyleTable
from util.constants import VOLT_S4_EASY


def main(page: Page) -> None:
    page.window_height = 600
    page.window_width = 800

    page.add(VoltStyleTable(VOLT_S4_EASY, expand=9))
    page.update()


if __name__ == "__main__":
    app(target=main)
