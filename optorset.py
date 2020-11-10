#!/usr/bin/env python
from __future__ import annotations

from array import array
from typing import Any
from typing import Set
from typing import Tuple
from uuid import UUID
from uuid import uuid4


class OptORSet:
    """
    Optimized Observed Remove set, or Opt-OR-Set
    """

    triple = Tuple[Any, int, int]
    E: Set[triple]
    V: array[int]
    _id: int

    def __init__(self, id: int, npeers: int):
        self.E = set()
        self.V = array("i", [0] * npeers)
        self._id = id

    def __str__(self) -> str:
        return f"OptORSet(E:{self.E}, V:{self.V})"

    def contains(self, element: Any) -> bool:
        return any(element in t for t in self.E)

    def elements(self) -> Set[Any]:
        return {e for e, _, _ in self.E}

    def add(self, element: Any) -> None:
        r = self._id
        c = self.V[r] + 1
        # pre causal delivery
        if c > self.V[r]:
            o = {
                (e, c2, i) for e, c2, i in self.E if c2 < c and e == element and i == r
            }
            self.V[r] = c
            self.E.add((element, c, r))
            self.E = self.E - o

    def remove(self, element: Any) -> None:
        R = {ele for ele in self.E if element in ele}
        # pre causal delivery
        self.E = self.E - R

    def compare(self, B: OptORSet) -> bool:
        R = {
            (c, i)
            for i, v in enumerate(self.V)
            for c in range(1, v + 1)
            if not (c, i) in ((c, i) for _, c, i in self.E)
        }
        R1 = {
            (c, i)
            for i, v in enumerate(B.V)
            for c in range(1, v + 1)
            if not (c, i) in ((c, i) for _, c, i in B.E)
        }
        return self.V <= B.V and R <= R1

    def merge(self, B: OptORSet) -> None:
        M = self.E & B.E
        M1 = {(e, c, i) for e, c, i in (self.E - B.E) if c > B.V[i]}
        M2 = {(e, c, i) for e, c, i in (B.E - self.E) if c > self.V[i]}
        U = M | M1 | M2
        O = {
            (e, c, i)
            for (e, c, i) in U
            if (e, i) in ((e, i) for e, c1, i in U if c < c1)
        }
        self.E = U - O
        self.V = array("i", [max(v, b) for v, b in zip(self.V, B.V)])


def main() -> int:

    ops0 = OptORSet(0, 2)
    ops1 = OptORSet(1, 2)

    print("ops0: add 1")
    ops0.add(1)
    print("compare", ops0.compare(ops1))
    ops1.merge(ops0)
    print("compare", ops0.compare(ops1))
    print("ops0: ", ops0)
    print("ops1: ", ops1)

    print("ops0: remove 1")
    ops0.remove(1)
    print("compare", ops0.compare(ops1))
    ops1.merge(ops0)
    print("compare", ops0.compare(ops1))
    print("ops0: ", ops0)
    print("ops1: ", ops1)

    print("ops0: add 1")
    ops0.add(1)
    print("compare", ops0.compare(ops1))
    ops1.merge(ops0)
    print("compare", ops0.compare(ops1))
    print("ops0: ", ops0)
    print("ops1: ", ops1)

    print("ops0: add 1")
    ops0.add(2)
    print("compare", ops0.compare(ops1))
    ops1.merge(ops0)
    print("compare", ops0.compare(ops1))
    print("ops0: ", ops0)
    print("ops1: ", ops1)

    return 0


if __name__ == "__main__":
    exit(main())
