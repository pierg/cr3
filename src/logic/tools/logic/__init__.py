import re
from typing import List

OPERATORS = r"\+|-|\*|==|<=|>=|<|>|!|\||->|&"
TEMPORAL_OPS = r"^F|^G|^X|^U"

operators = re.compile(OPERATORS)
temporal_ops = re.compile(TEMPORAL_OPS)


class Logic:
    @staticmethod
    def general(operation: str, elements: List[str]):
        if operation == "And":
            return Logic.and_(elements, brackets=True)
        elif operation == "Or":
            return Logic.or_(elements)
        elif operation == "Not":
            return Logic.not_(elements[0])
        elif operation == "Implies":
            return Logic.implies_(elements[0], elements[1])
        else:
            raise Exception(f"Attribute unknown: {operation}")

    @staticmethod
    def and_(propositions: List[str], brackets: bool = False) -> str:
        """Returns an str formula representing the logical AND of
        list_propoositions."""
        if len(propositions) > 1:

            if "FALSE" in propositions:
                return "FALSE"
            """Remove all TRUE elements"""
            propositions = list(filter("TRUE".__ne__, propositions))
            if len(propositions) == 0:
                return "TRUE"

            conj = " & ".join(propositions)
            if brackets:
                return f"({conj})"
            else:
                return conj

        elif len(propositions) == 1:
            return propositions[0]
        else:
            raise Exception("List of propositions is empty")

    @staticmethod
    def implies_(prop_1: str, prop_2: str) -> str:
        """Returns an str formula representing the logical IMPLIES of prop_1
        and prop_2."""
        if (
            prop_1 == "TRUE"
            or prop_1 == "(TRUE)"
            or prop_1 == "true"
            or prop_1 == "(true)"
        ):
            return prop_2
        return f"(({prop_1}) -> ({prop_2}))"
        # return f"(!({prop_1}) | ({prop_2}))"

    @staticmethod
    def iff_(prop_1: str, prop_2: str) -> str:
        """Returns an str formula representing the logical IFF of prop_1 and
        prop_2."""
        if (
            prop_1 == "TRUE"
            or prop_1 == "(TRUE)"
            or prop_1 == "true"
            or prop_1 == "(true)"
        ):
            return prop_2
        return f"(({prop_1}) <-> ({prop_2}))"

    @staticmethod
    def not_(prop: str) -> str:
        """Returns an str formula representing the logical NOT of prop."""
        # match_operators = bool(re.search(operators, prop))
        # match_temporal = bool(re.search(temporal_ops, prop))
        # if match_operators or match_temporal:
        #     return f"!({prop})"
        if prop == "TRUE":
            return "FALSE"
        if prop == "FALSE":
            return "TRUE"
        return f"!({prop})"

    @staticmethod
    def x_(prop: str) -> str:
        """Next."""
        return f"X({prop})"

    @staticmethod
    def xn_(prop: str, n: int) -> str:
        """n times Next."""
        ret = ""
        for i in range(n):
            ret += "X("
        ret += prop
        for i in range(n):
            ret += ")"
        return ret

    @staticmethod
    def f_(prop: str) -> str:
        """Eventually."""
        return f"F({prop})"

    @staticmethod
    def g_(prop: str) -> str:
        """Globally."""
        return f"G({prop})"

    @staticmethod
    def gf_(prop: str) -> str:
        """Globally Eventually."""
        return f"G(F({prop}))"

    @staticmethod
    def u_(pre: str, post: str) -> str:
        """Until."""
        return f"({pre} U {post})"

    @staticmethod
    def w_(pre: str, post: str) -> str:
        """Weak Until."""
        return Logic.or_([Logic.u_(pre, post), Logic.g_(pre)])

    @staticmethod
    def or_(propositions: List[str], brackets=True) -> str:
        """Returns an formula formula representing the logical OR of
        list_propoositions."""
        if len(propositions) > 1:
            if "TRUE" in propositions:
                return "TRUE"
            """Remove all FALSE elements"""
            propositions = list(filter("FALSE".__ne__, propositions))

            res = " | ".join(propositions)
            if brackets:
                return f"({res})"
            else:
                return f"{res}"
        elif len(propositions) == 1:
            return propositions[0]
        else:
            raise Exception("List of propositions is empty")
