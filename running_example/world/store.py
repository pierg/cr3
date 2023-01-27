from synthesis.world import World
from logic.typelement.robotic import BooleanAction, BooleanLocation, BooleanSensor
from logic.typeset import Typeset

project_name = "running_example"

w_abstract = World(
    project_name=project_name,
    typeset=Typeset(
        {
            BooleanLocation(
                name="lf",
                description="front",
                mutex_group="abstract_locs",
                adjacency_set={"lb"},
            ),
            BooleanLocation(
                name="lb",
                description="back",
                mutex_group="abstract_locs",
                adjacency_set={"lf"},
            ),
            BooleanLocation(
                name="le",
                description="entrance",
                refinement_of={"lf"}),
            BooleanSensor(
                name="s",
                description="person detected"),
            BooleanAction(
                name="g",
                description="greeting"),
        }
    ),
)

w_refined = World(
    project_name=project_name,
    typeset=Typeset(
        {
            BooleanLocation(
                name="l1",
                mutex_group="locations",
                adjacency_set={"l3", "l2"},
                refinement_of={"lf"},
            ),
            BooleanLocation(
                name="l2",
                mutex_group="locations",
                adjacency_set={"l1", "l4"},
                refinement_of={"le"},
            ),
            BooleanLocation(
                name="l3",
                mutex_group="locations",
                adjacency_set={"l1", "l4", "l5"},
                refinement_of={"lf"},
            ),
            BooleanLocation(
                name="l4",
                mutex_group="locations",
                adjacency_set={"l3", "l2"},
                refinement_of={"lf"},
            ),
            BooleanLocation(
                name="l5",
                mutex_group="locations",
                adjacency_set={"l3"},
                refinement_of={"lb"},
            ),
        }
    ),
)
