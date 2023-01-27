from running_example.library.library import library_goals
from running_example.world.store import w_abstract
from repair.utils.library import get_candidate_composition
from goals.goal import Goal
from goals.library import Library
from contracts.contract import Contract
from logic.patterns.robotic_movement import OrderedPatrolling
from logic.specification.temporal import LTL


project_name = "running_example"


goal_to_refine = Goal(
    id="ordered_patrolling",
    contract=Contract(
        _guarantees=LTL(f'{OrderedPatrolling(["lf", "lb"])}', w_abstract.typeset)
    ),
    world=w_abstract,
)

print(goal_to_refine)

library = Library(library_goals)


candidate_composition = get_candidate_composition(library=library,
                                                  goal_to_refine=goal_to_refine)


print(candidate_composition)

print(candidate_composition.contract <= goal_to_refine.contract)


