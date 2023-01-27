from running_example.candidate_composition import goal_to_refine, candidate_composition
from running_example.library.library import library_goals_2
from goals.goal.operations.quotient import g_quotient
from goals.library import Library

project_name = "running_example"

"""We have computed in 'candidate_composition.py' """

assert not candidate_composition <= goal_to_refine

library_2 = Library(library_goals_2)

quotient = g_quotient(goal_to_refine, candidate_composition)

lib_5 = list(filter(lambda g: g.id == "lib_5", library_goals_2))[0]

assert lib_5.contract.guarantees <= quotient.contract.guarantees

assert lib_5 <= quotient

# print([g.id == "lib_5" for g in library_goals_2])
#
# assert not list(filter(lambda g: g.id == "lib_5", library_goals_2))[0] <= quotient
#
# result = get_candidate_composition(library_2, quotient)
#
# assert result <= quotient
#
# print(result)