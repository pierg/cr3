from goals.cgg import Cgg, Link
from goals.context import group_conjunction
from contracts.contract.exceptions import ContractException
from goals.goal import Goal
from goals.goal.exceptions import GoalAlgebraOperationFail, GoalFailOperations
from goals.goal.operations._shared import (
    GoalOperation,
    generate_goal_operations_name_description,
    generate_shared_world,
)
from contracts.operations.merging import merging


def g_merging(goals: set[Goal], cgg: Cgg | None = None) -> Goal:
    if len(goals) == 1:
        return next(iter(goals))
    if len(goals) == 0:
        raise Exception("No goal specified in the merging")

    world = generate_shared_world(goals)

    id, description = generate_goal_operations_name_description(
        list(goals), GoalOperation.Merging
    )

    context = group_conjunction(set(map(lambda g: g.context, goals)))

    try:
        contract = merging(set(map(lambda g: g.contract, goals)))

    except ContractException as e:

        raise GoalAlgebraOperationFail(
            goals=goals, operation=GoalFailOperations.merging, contr_ex=e
        )

    goal = Goal(
        contract=contract,
        id=id,
        description=description,
        context=context,
        world=world,
    )

    goals_ids = ", ".join(g.id for g in goals)
    print(f"{goal.id} -- merging of -- {goals_ids}")
    # Fix Cgg
    # if cgg is not None:
    #     for g in goals:
    #         cgg.add_edge(node_a=g, node_b=goal, link=Link.merging)

    return goal
