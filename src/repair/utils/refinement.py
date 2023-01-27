import itertools
from collections import Counter

from goals.goal import Goal


def get_most_refined(goals: list[Goal]) -> Goal:
    if len(goals) == 1:
        return goals[0]

    scores = Counter()

    for g in goals:
        scores[g] = 0
    for a, b in itertools.permutations(goals, 2):
        if a <= b:
            scores[a] += 1

    for goal, count in scores.items():
        scores[goal] = count / len(goals) * 100

    print("ratings")
    print([g.id for g in goals])
    for goal, count in scores.items():
        print(f"{goal.id}: {count}")

    return scores.most_common(1)[0][0]