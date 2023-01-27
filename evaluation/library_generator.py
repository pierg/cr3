import random
import time

from contracts.contract import Contract
from logic.specification.temporal import LTL
from logic.typelement.basic import BooleanControllable
from logic.typeset import Typeset


def spec_generator(n_clauses: int = 5) :
    spec: LTL = LTL("TRUE")
    specs: list[LTL] = []
    i = 0
    for j in range(0, n_clauses):
        clause_options = [
            f"G(F(pa) & F(pb & F(pc)))",
            f"G(F(pa) U (pb & X(pc)))",
            f"G(F(pa) U (pb | X(pc)))",
            f"G(F(pa) U (F(pb) & X(pc)))"
        ]
        clause_chosen = random.choice(clause_options)
        p1, p2, p3 = f"p{i}", f"p{i + 1}", f"p{i + 2}"
        b1, b2, b3 = BooleanControllable(name=p1), BooleanControllable(name=p2), BooleanControllable(name=p3)
        clause_formula = clause_chosen.replace("pa", p1).replace("pb", p2).replace("pc", p3)
        clause = LTL(clause_formula, Typeset({b1, b2, b3}))
        spec &= clause
        specs.append(clause)
        i += 3



    start_time = time.time()
    clauses_contracts: list[Contract] = [Contract(spec) for spec in specs]
    end_time = time.time()
    clause_time = end_time - start_time

    print(clause_time)


    start_time = time.time()
    mono_contract: Contract = Contract(spec)
    end_time = time.time()
    mono_time = end_time - start_time

    print(mono_time)
    print(clause_time)
    print(clause_time/mono_time)


if __name__ == '__main__':
    spec_generator()
