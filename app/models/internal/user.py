import json

class User:
    __slots__ = ["parent", "uid", "intr_grp"]

    def __init__(self, parent: "User|None", uid: str, intr_grp: set):
        self.parent: "User" = parent if parent else self
        self.uid: str = uid
        self.intr_grp: set["User"] = intr_grp

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, User):
            return False

        self_parent_uid = self.parent.uid if self.parent else None
        other_parent_uid = other.parent.uid if other.parent else None

        if self_parent_uid != other_parent_uid:
            return False
        
        if self.uid != other.uid:
            return False

        self_ids = {user.uid for user in self.intr_grp}
        other_ids = {user.uid for user in other.intr_grp}

        return self_ids == other_ids
    
    def traverse(self) -> set[str]:
        uids: set[str] = {self.uid}
        visited: set["User"] = {self}
        to_visit: set["User"] = self.intr_grp

        while to_visit:
            current = to_visit.pop()
            visited.add(current)
            uids.add(current.uid)
            will_visit = current.intr_grp.difference(visited, to_visit)
            to_visit.update(will_visit)
        return uids
    
    def __hash__(self) -> int:
        return hash(self.uid)
    
    def __repr__(self) -> str:
        return json.dumps({"parent": self.parent.uid, "uid": self.uid, "intr_grp":[user.uid for user in self.intr_grp]})