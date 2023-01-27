from contracts.contract import Contract
from running_example.world.store import w_refined
from goals.goal import Goal
from goals.goal.operations.merging import g_merging
from goals.goal.operations.separation import g_separation
from logic.specification.temporal import LTL
from logic.typelement.robotic import BooleanSensor, BooleanAction
from logic.typeset import Typeset
from synthesis.world import World

project_name = "running_example"

w_greeting = World(
    project_name=project_name,
    typeset=Typeset(
        {
            BooleanSensor(
                name="s",
                description="sensor"
            ),
            BooleanAction(
                name="g",
                description="greeting"
            ),
        }
    ),
)

"""We have computed in 'candidate_composition.py' """

goal_to_refine = Goal(
    id="g_to_ref",
    contract=Contract(_assumptions=LTL("GF(s)", w_greeting.typeset),
                      _guarantees=LTL("G(s->g)", w_greeting.typeset)))

goal_from_library = Goal(
    id="lib_goal",
    contract=Contract(_guarantees=LTL("G(s->Xg)", w_greeting.typeset)))

assert not goal_from_library <= goal_to_refine

separation = g_separation(goal_from_library, goal_to_refine)

print(separation)

goal_to_refine = g_merging({separation, goal_to_refine})

assert goal_from_library <= goal_to_refine
