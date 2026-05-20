from dataclasses import dataclass

@dataclass
class User:
    __slots__ = ['parent', 'intr_grp']
    parent: str
    intr_grp: list[str]
