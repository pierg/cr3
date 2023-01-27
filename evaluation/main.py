import time

from contracts.contract import Contract
from evaluation.spec_generator import spec_generator
from goals.goal import Goal

if __name__ == '__main__':
    spec, specs = spec_generator(5)

    clauses_contracts: list[Contract] = [Contract(spec, _skip_sat=True) for spec in specs]
    mono_contract: Contract = Contract(spec, _skip_sat=True)

    clauses_goals: list[Goal] = [Goal(contract) for contract in clauses_contracts]
    mono_goal: Goal = Goal(mono_contract)

    for g in clauses_goals:
        g.realize()
    clauses_synth_time = sum([g.controller.synth_time for g in clauses_goals])
    print(clauses_synth_time)


    mono_goal.realize()
    mono_synth_time = mono_goal.controller.synth_time
    print(mono_synth_time)
    print(clauses_synth_time)
    print(clauses_synth_time / mono_synth_time)
