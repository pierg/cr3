from __future__ import annotations

import itertools
from dataclasses import dataclass
from functools import reduce

from goals.goal import Goal
from goals.goal.operations.composition import g_composition
from logic.typeset import Typeset


@dataclass
class Library:
    goals: set[Goal]

    @property
    def typeset(self) -> Typeset:
        typeset = Typeset()
        for goal in self.goals:
            typeset += goal.contract.typeset
        return typeset

    def search_refinement(self, goal_to_refine: Goal) -> Goal | None:
        """Finds a composition of goals that refine 'goal_to_refine'.

        MOCK UP OF GREEDY ALGORITHM IN COGOMO, TODO: integrate here
        """

        print(f"Searching refinements for {goal_to_refine.id}")

        for n in range(1, len(self.goals)):
            for subset in itertools.combinations(self.goals, n):
                if len(subset) == 1:
                    subset_typeset = subset[0].contract.typeset
                else:
                    subset_typeset = reduce(
                        (lambda x, y: x | y), [g.contract.typeset for g in subset]
                    )
                if not self.covers(goal_to_refine, subset_typeset)[0]:
                    continue
                g = g_composition(subset)
                print(f"Composition:\n{g}")
                if g.contract <= goal_to_refine.contract:
                    return g

        return None

    def covers(self, goal: Goal) -> float:
        """Returns the percentage of "coverage" of the library to 'goal'. I.e. the ratio of how many types are similar"""
        return self.typeset.similarity_score(goal.contract.typeset)
