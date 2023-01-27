from logic.specification.temporal import LTL
from logic.typelement.basic import BooleanControllable
from logic.typeset import Typeset


def spec_library_generator(max_number_clauses: int = 5) -> list[LTL]:
    specs: list[LTL] = []
    i = 0
    for j in range(0, max_number_clauses):
        clause_options = [
            f"G(F(pa) & F(pb & F(pc)))",
            f"G(F(pa) U (pb & X(pc)))",
            f"G(F(pa) U (pb | X(pc)))",
            f"G(F(pa) U (F(pb) & X(pc)))"
        ]
        for clause_option in clause_options:
            p1, p2, p3 = f"p{i}", f"p{i + 1}", f"p{i + 2}"
            b1, b2, b3 = BooleanControllable(name=p1), BooleanControllable(name=p2), BooleanControllable(name=p3)
            clause_formula = clause_option.replace("pa", p1).replace("pb", p2).replace("pc", p3)
            clause = LTL(clause_formula, Typeset({b1, b2, b3}))
            specs.append(clause)
        i += 3

    return specs


def trivial_library_search