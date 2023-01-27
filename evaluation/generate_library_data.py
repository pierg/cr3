from contracts.contract import Contract
from evaluation.spec_generator import spec_generator
from evaluation.utils import save_lists_to_files
from goals.goal import Goal
from logic.specification.temporal import LTL


def get_synth_time(spec: LTL, specs: list[LTL]) -> tuple[float, float]:
    clauses_contracts: list[Contract] = [Contract(spec, _skip_sat=True) for spec in specs]
    mono_contract: Contract = Contract(spec, _skip_sat=True)

    clauses_goals: list[Goal] = [Goal(contract) for contract in clauses_contracts]
    mono_goal: Goal = Goal(mono_contract)

    for g in clauses_goals:
        g.realize()
    clauses_synth_time = sum([g.controller.synth_time for g in clauses_goals])
    mono_goal.realize()
    mono_synth_time = mono_goal.controller.synth_time

    return mono_synth_time, clauses_synth_time


def gen_times_for(min_clauses: int = 1, max_clauses: int = 500):
    x = []
    ya = []
    yb = []
    for i in range(min_clauses, max_clauses):
        spec, specs = spec_generator(i)
        mono_synth_time, clauses_synth_time = get_synth_time(spec, specs)
        x.append(i)
        ya.append(mono_synth_time)
        yb.append(clauses_synth_time)
        save_lists_to_files(x, ya, yb)


if __name__ == '__main__':
    gen_times_for()
