#!/usr/bin/env python
from __future__ import annotations

from typing import Any
from typing import Set
from typing import Tuple
from uuid import UUID
from uuid import uuid4


class ORSet:
    """
    Observed Remove Set, or OR-Set is an add-wins replicated set CRDT
    """

    Elements: Set[Tuple[Any, UUID]]
    Tombstones: Set[Tuple[Any, UUID]]

    def __init__(self):
        self.Elements = set()
        self.Tombstones = set()

    def __str__(self) -> str:
        return f"ORSet(Elements:{self.Elements}, Tombstones:{self.Tombstones})"

    def contains(self, element: Any) -> bool:
        return any(element in t for t in self.Elements)

    def elements(self) -> Set[Any]:
        return {e for e, _ in self.Elements}

    def add(self, element: Any) -> None:
        self.Elements.add((element, uuid4()))
        self.Elements = self.Elements - self.Tombstones

    def remove(self, element: Any) -> None:
        r = {ele for ele in self.Elements if element in ele}
        self.Elements = self.Elements - r
        self.Tombstones |= r

    def compare(self, B: ORSet) -> bool:
        elems = B.Elements | B.Tombstones
        tombstones = self.Elements | self.Tombstones
        return elems <= B.Elements and tombstones <= B.Tombstones

    def merge(self, B: ORSet) -> None:
        self.Elements = self.Elements - B.Elements
        self.Elements |= B.Elements - self.Tombstones
        self.Tombstones |= B.Tombstones


def main() -> int:
    ors0 = ORSet()
    ors1 = ORSet()

    print("ors0: add 1")
    ors0.add(1)
    print("compare", ors0.compare(ors1))
    ors1.merge(ors0)
    print("compare", ors0.compare(ors1))
    print("ors0: ", ors0)
    print("ors1: ", ors1)

    print("ors0: remove 1")
    ors0.remove(1)
    print("compare", ors0.compare(ors1))
    ors1.merge(ors0)
    print("compare", ors0.compare(ors1))
    print("ors0: ", ors0)
    print("ors1: ", ors1)

    print("ors0: add 1")
    ors0.add(1)
    print("compare", ors0.compare(ors1))
    ors1.merge(ors0)
    print("compare", ors0.compare(ors1))
    print("ors0: ", ors0)
    print("ors1: ", ors1)

    print("ors0: add 1")
    ors0.add(2)
    print("compare", ors0.compare(ors1))
    ors1.merge(ors0)
    print("compare", ors0.compare(ors1))
    print("ors0: ", ors0)
    print("ors1: ", ors1)

    return 0


if __name__ == "__main__":
    exit(main())
