from repair.utils.refinement import get_most_refined
from goals.library import Library
import itertools
from collections import Counter
from functools import reduce

from goals.goal import Goal
from goals.goal.operations.composition import g_composition
from logic.typeset import Typeset


def get_candidate_composition(library: Library, goal_to_refine: Goal):
    candidates = Counter()
    best_similarity_score = 0

    for n in range(1, len(library.goals)):
        for subset in itertools.combinations(library.goals, n):
            n_compositions = len(subset)
            if n_compositions == 1:
                subset_typeset = subset[0].contract.typeset
            else:
                subset_typeset = reduce(
                    (lambda x, y: x + y), [g.contract.typeset for g in subset]
                )

            if "lib_1" in [g.id for g in subset] and "lib_2" in [g.id for g in subset]:
                print("wait")
            similarity_score = subset_typeset.similarity_score(
                goal_to_refine.contract.typeset
            )
            print(similarity_score)
            print(str([g.id for g in subset]) + f"\t{similarity_score}")
            if similarity_score > best_similarity_score:
                candidates = Counter()
                best_similarity_score = similarity_score
            elif similarity_score == best_similarity_score:
                candidates[g_composition(set(subset))] = n_compositions

    print(
        f"There are {len(candidates.keys())} candidates with the same number of similar types: {best_similarity_score}"
    )

    for goal, count in candidates.items():
        print(f"{goal.id}: {count}")

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
