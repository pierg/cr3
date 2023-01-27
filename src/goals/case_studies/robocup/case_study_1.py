from goals.case_studies.robocup.world.world_ref import w_ref
from goals.case_studies.robocup.world.world_top import w_top
from contracts.contract import Contract
from goals.goal import Goal
from logic.patterns.robotic_movement import *
from logic.specification.temporal import LTL

g_top = Goal(
    id="order_patrol",
    contract=Contract(
        _guarantees=LTL(StrictOrderedPatrolling(["lb", "lv"]), _typeset=w_top.typeset)
    ),
    world=w_top,
)

g_ref = Goal(
    id="order_patrol_ref",
    contract=Contract(
        _guarantees=LTL(StrictOrderedPatrolling(["b2", "l2"]), _typeset=w_ref.typeset)
    ),
    world=w_ref,
)

assert g_ref.contract <= g_top.contract
