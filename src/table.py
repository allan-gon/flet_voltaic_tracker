# built-in
from os.path import abspath
from json import load

# packages
from flet import (
    Row,
    Column,
    Container,
    Text,
    UserControl,
)
from flet_core.alignment import center, center_left

# my code
from util.constants import VERTICAL


class VoltStyleTable(UserControl):
    def __init__(self, path_to_file, expand=True):
        super().__init__()
        with open(abspath(path_to_file)) as file:
            schema = load(file)

        self.types = schema["types"]
        self.ranks = schema["ranks"]
        self.expand = expand

    def build(self):
        self.table = Row(expand=True)
        # containers for cells
        types = Column(controls=[Container(expand=1, bgcolor="#4A36DE")], expand=1)
        sub_types = Column(controls=[Container(expand=1, bgcolor="#4A36DE")], expand=1)
        scenarios = Column(
            controls=[
                Container(
                    expand=True,
                    bgcolor="#4A36DE",
                    content=Text(value="Scenario"),
                    alignment=center,
                )
            ],
            expand=8,
        )
        high_scores = Column(
            controls=[
                Container(
                    expand=True,
                    bgcolor="#4A36DE",
                    content=Text(value="High Score"),
                    alignment=center,
                )
            ],
            expand=4,
        )
        benchmarks = []
        for idx, rank_dict in enumerate(self.ranks):
            benchmarks.append(Column(expand=4))
            benchmarks[idx].controls.append(
                Container(
                    expand=True,
                    bgcolor=rank_dict["header_color"],
                    content=Text(value=rank_dict["name"]),
                    alignment=center,
                )
            )

        for type_dict in self.types:
            # access the only key
            scen_type = type_dict["name"]
            # save the scenario type cell
            types.controls.append(
                Container(
                    # assumed 2 scenarios per subtype
                    expand=len(type_dict["subtypes"]) * 2,
                    bgcolor=type_dict["color"],
                    content=Text(
                        value=scen_type,
                        rotate=VERTICAL,
                        no_wrap=True,
                    ),
                    alignment=center,
                )
            )
            # subtype
            for sub_type_dict in type_dict["subtypes"]:
                # access the only key
                sub_type = sub_type_dict["name"]
                # save the scenario sub type
                sub_types.controls.append(
                    Container(
                        expand=2,
                        bgcolor=sub_type_dict["color"],
                        content=Text(value=sub_type, rotate=VERTICAL, no_wrap=True),
                        alignment=center,
                    )
                )
                # scenario
                for scen_dict in sub_type_dict["scenarios"]:
                    # access the only key
                    scenario = scen_dict["name"]
                    # save the scenario
                    scenarios.controls.append(
                        Container(
                            expand=True,
                            bgcolor=sub_type_dict["scenario_color"],
                            content=Text(
                                value=scenario,
                                color="black",
                            ),
                            alignment=center_left,
                            padding=5,
                        )
                    )
                    # high score placeholder
                    high_scores.controls.append(
                        Container(
                            expand=True,
                            bgcolor="white",
                            content=Text(color="black"),
                            alignment=center,
                        )
                    )
                    for idx, score in enumerate(scen_dict["scores"]):
                        benchmarks[idx].controls.append(
                            Container(
                                expand=True,
                                bgcolor=self.ranks[idx]["other_color"],
                                content=Text(value=score, color="black"),
                                alignment=center,
                            )
                        )
                    # TODO: highscore

        self.table.controls.append(types)
        self.table.controls.append(sub_types)
        self.table.controls.append(scenarios)
        self.table.controls.append(high_scores)
        for benchmark in benchmarks:
            self.table.controls.append(benchmark)
        return self.table
