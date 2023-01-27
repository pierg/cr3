from goals.goal import Goal
from goals.goal.operations.merging import g_merging
from goals.goal.operations.separation import g_separation
from contracts.contract import Contract
from logic.specification.temporal import LTL

top_spec = Goal(contract=Contract(_assumptions=LTL("a1"), _guarantees=LTL("g1")))

print(f"TOP_SPEC:\n{top_spec}")

lib_spec = Goal(contract=Contract(_assumptions=LTL("a2"), _guarantees=LTL("g2")))


print(f"LIB_SPEC:\n{lib_spec}")


sep = g_separation(lib_spec, top_spec)
print(f"M1:\n{sep}")


new = g_merging({top_spec, sep})
print(f"M2:\n{new}")

print(new.contract.assumptions.boolean.dnf)
print(new.contract.guarantees.boolean.cnf)
