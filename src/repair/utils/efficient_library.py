from random import random

from repair.utils.refinement import get_most_refined
from goals.library import Library
import itertools
from collections import Counter
from functools import reduce

from goals.goal import Goal
from goals.goal.operations.composition import g_composition
from logic.typeset import Typeset


def maximize_coverage(types_to_cover: set[str],
                      library_elements: dict[str, set[str]]):
    print("maximising coverage...")
    disjoint_combinations = []
    for key in types_to_cover:
        disjoint_combinations.append(set(elem for elem in library_elements if key in library_elements[elem]))
    # Create a list of all possible combinations of elements
    element_combinations = list(itertools.product(*disjoint_combinations))
    # Create a dictionary to store the coverage of each combination
    coverage = {}
    for comb in element_combinations:
        coverage[comb] = set()
        for element in comb:
            coverage[comb] |= library_elements[element]
    # Sort the combinations by coverage in decreasing order
    sorted_combinations = sorted(coverage, key=lambda x: len(coverage[x]), reverse=True)

    return sorted_combinations



def get_candidate_composition_efficient(library: dict[str, Goal], goal_to_refine: Goal, evaluation: bool = False):
    print(f"Searching among {len(library)} elements...")
    candidates = Counter()
    best_similarity_score = 0

    types_to_cover = set(t.name for t in list(goal_to_refine.contract.typeset.values()))
    library_elements = {}
    for id, goal in library.items():
        library_elements[id] =  set(t.name for t in list(goal.contract.typeset.values()))

    sorted_combinations = maximize_coverage(types_to_cover, library_elements)

    for i, b in sorted_combinations.items():
        print(f"{i}: {b}")

    for n in range(1, len(library.goals)):
        for subset in itertools.combinations(library.goals, n):
            n_compositions = len(subset)
            if n_compositions == 1:
                subset_typeset = subset[0].contract.typeset
            else:
                subset_typeset = reduce(
                    (lambda x, y: x + y), [g.contract.typeset for g in subset]
                )

            similarity_score = subset_typeset.similarity_score(
                goal_to_refine.contract.typeset
            )
            if similarity_score == 0:
                continue

            if similarity_score > best_similarity_score:
                candidates: dict[int, list[Goal]] = {}
                best_similarity_score = similarity_score

            if similarity_score == best_similarity_score:
                candidates[n_compositions] = list(subset)

    if evaluation:
        return len(candidates), best_similarity_score

                # candidates[g_composition(set(subset))] = n_compositions

    # print(
    #     f"There are {len(candidates.keys())} candidates with the same number of similar types: {best_similarity_score}"
    # )

    # for goal, count in candidates.items():
    #     print(f"{goal.id}: {count}")

    # Filtering candidates with too many goals composed
    new_candidates = [
        x for x, count in candidates.items() if count == min(candidates.values())
    ]

    print("filtering...")
    print("\n".join(e.id for e in new_candidates))

    winner = get_most_refined(new_candidates)
    print(f"{winner.id} is the most refined candidate")

    return winner


def search_refinement(library: Library, goal_to_refine: Goal) -> Goal | None:
    """
    Finds a composition of goals that refine 'goal_to_refine'.
    """

    print(f"Searching refinements for {goal_to_refine.id}")

    for n in range(1, len(library.goals)):
        for subset in itertools.combinations(library.goals, n):
            if len(subset) == 1:
                subset_typeset = subset[0].contract.typeset
            else:
                subset_typeset = reduce(
                    (lambda x, y: x | y), [g.contract.typeset for g in subset]
                )
            if not similarity_score(library, subset_typeset):
                continue
            g = g_composition(subset)
            print(f"Composition:\n{g}")
            if g.contract <= goal_to_refine.contract:
                return g

    return None


def similarity_score(library: Library, typeset: Typeset) -> float:
    """Returns the percentage of "coverage" of the library to the typeset"""
    return library.typeset.similarity_score(typeset)


def covering(library: Library, goal: Goal) -> float:
    """Returns the percentage of "coverage" of the library to 'goal'. I.e. the ratio of how many types are similar"""
    return library.typeset.similarity_score(goal.contract.typeset)
