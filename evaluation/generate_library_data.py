import time

from contracts.contract import Contract
from evaluation.spec_generator import spec_generator
from evaluation.utils import save_lists_to_files
from goals.goal import Goal
from goals.library import Library
from logic.specification.temporal import LTL
from repair.utils.efficient_library import get_candidate_composition_efficient
from repair.utils.library import get_candidate_composition


def get_search_time(spec: LTL, lib_specs: list[LTL]) -> tuple[float, int, int]:
    spec_contract: Contract = Contract(spec, _skip_sat=True)
    spec_goal: Goal = Goal(spec_contract)

    library_contracts: list[Contract] = [Contract(spec, _skip_sat=True) for spec in lib_specs]
    library_goals: list[Goal] = [Goal(contract) for contract in library_contracts]

    # library = Library(set(library_goals))
    library = {g.id: g for g in library_goals}
    time_elapsed, n_candidates, similarity_score = get_candidate_composition_efficient(library, spec_goal, evaluation=True)

    return time_elapsed, n_candidates, similarity_score


def gen_times_for(min_clauses: int = 1, max_clauses: int = 500):
    x = []
    ya = []
    yb = []
    for i in range(min_clauses, max_clauses):
        spec, specs = spec_generator(i)
        spec_synth_time, library_synth_time = get_search_time(spec, specs)
        x.append(i)
        ya.append(spec_synth_time)
        yb.append(library_synth_time)
        save_lists_to_files(x, ya, yb)


if __name__ == '__main__':
    gen_times_for()
