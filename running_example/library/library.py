from running_example.world.store import w_refined
from goals.goal import Goal
from contracts.contract import Contract
from logic.patterns.robotic_movement import Patrolling, Visit, StrictOrderedLocations
from logic.specification.temporal import LTL

library_goals = {
    Goal(
        id="lib_1",
        contract=Contract(LTL(Patrolling(["l5"]), w_refined.typeset)),
        world=w_refined,
    ),
    Goal(
        id="lib_2",
        contract=Contract(LTL(Patrolling(["l3"]), w_refined.typeset)),
        world=w_refined,
    ),
    Goal(
        id="lib_3",
        contract=Contract(LTL(Visit(["l3", "l1"]), w_refined.typeset)),
        world=w_refined,
    ),
    Goal(
        id="lib_4",
        contract=Contract(LTL(Visit(["l5"]), w_refined.typeset)),
        world=w_refined,
    ),
}


library_goals_2 = {
    Goal(
        id="lib_1",
        contract=Contract(LTL(Patrolling(["l5"]), w_refined.typeset)),
        world=w_refined,
    ),
    Goal(
        id="lib_2",
        contract=Contract(LTL(Patrolling(["l3"]), w_refined.typeset)),
        world=w_refined,
    ),
    Goal(
        id="lib_3",
        contract=Contract(LTL(Visit(["l3", "l1"]), w_refined.typeset)),
        world=w_refined,
    ),
    Goal(
        id="lib_4",
        contract=Contract(LTL(Visit(["l5"]), w_refined.typeset)),
        world=w_refined,
    ),
    Goal(
        id="lib_5",
        contract=Contract(LTL(StrictOrderedLocations(["l3", "l5"]), w_refined.typeset)),
        world=w_refined,
    ),
}