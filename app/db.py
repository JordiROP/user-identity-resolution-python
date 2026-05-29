from app.models.internal.interaction import Interaction
from app.models.internal.user import User
from app.models.internal.metrics import Metric
from app.models.commons.values import Source, Event

class DB:
    __slots__ = ["interactions", "users", "user_interaction", "metrics", "recompute"]

    def __init__(self):
        self.interactions: dict[str, Interaction] = {}
        self.users: dict[str, User] = {}
        self.user_interaction: dict[str, list[str]] = {}
        self.metrics: dict[str, Metric] = {}
        self.recompute: set[str] = set()

    def user_exist(self, user_id: str) -> bool:
        return user_id in self.users

    def add_user(
        self, user_id: str, parent: User | None, users_gp: set[User]
    ) -> User:
        user = User(parent, user_id, users_gp)
        self.users[user_id] = user
        return user
    
    def get_user(self, user_id: str) -> User:
        return self.users[user_id]

    def get_parent(self, user_id) -> User:
        current: str = user_id
        parent: User = self.users[current].parent

        while parent.uid != current:
            current = parent.uid
            parent = self.users[current].parent

        self.users[current].parent = parent
        return parent

    def update_usr_intr_grp(self, uid:str, usr_grp: set[User], truncate: bool = False):
        if truncate:
            self.users[uid].intr_grp = usr_grp
        else:
            self.users[uid].intr_grp.update(usr_grp)

    def get_interaction(self, iuid: str) -> Interaction:
        return self.interactions[iuid]

    def add_interaction(self, iuid: str, uids: set[str], source:str, event:str) -> None:
        self.interactions[iuid] = Interaction(uids, Source(source) , Event(event))

    def add_user_interaction(self, user_id: str, interaction_id: str) -> None:
        if user_id in db.user_interaction:
            db.user_interaction[user_id].append(interaction_id)
        else:
            db.user_interaction[user_id] = [interaction_id]

    def update_users_interaction(self, interaction_id: str, users: set[str]) -> None:
        db.interactions[interaction_id].user_ids = users

    def has_metrics(self, uid: str) -> bool:
        return uid in self.metrics
    
    def get_metric(self, uid: str) -> Metric:
        return self.metrics[uid]
    
    def create_metric(self, uid: str, source: Source, event: Event) -> Metric:
        metric = Metric(source, event)
        self.metrics[uid] = metric
        return metric
    
    def delete_metric(self, uid: str) -> None:
        del self.metrics[uid]
    
    def add_recompute(self, users: set[str]) -> None:
        self.recompute.update(users)

    def is_in_recompute(self, user_id: str) -> bool:
        return user_id in self.recompute 


db = DB()
