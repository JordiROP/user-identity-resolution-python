from app.models.internal.interaction import Interaction
from app.models.internal.user import User
from app.models.internal.metrics import Metric
from app.models.commons.values import Source, Event

from threading import RLock

class DB:
    __slots__ = ["interactions", "users", "user_interaction", "metrics", "unique_users", "bounced_users", "x_device_users", "_lock"]

    def __init__(self):
        self.interactions: dict[str, Interaction] = {}
        self.users: dict[str, User] = {}
        self.user_interaction: dict[str, set[str]] = {}
        self.metrics: dict[str, Metric] = {}

        self.unique_users:int = 0
        self.bounced_users:int = 0
        self.x_device_users:int = 0

        self._lock = RLock()

    def user_exist(self, user_id: str) -> bool:
        return user_id in self.users

    def add_user(
        self, user_id: str, parent: User | None, users_gp: set[User]
    ) -> User:
        user = User(parent, user_id, users_gp)
        self.users[user_id] = user
        return user
    
    def add_parent(self, uid: str, parent: User) -> None:
        db.users[uid].parent = parent

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
            db.user_interaction[user_id].add(interaction_id)
        else:
            db.user_interaction[user_id] = {interaction_id}

    def get_interaction_from_user(self, uid: str) -> set[str]:
        return set(self.user_interaction[uid])

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
    
    def delete_user(self, uid: str) -> None:
        del self.users[uid]
        del self.user_interaction[uid]
        if uid in self.metrics:
            del self.metrics[uid]
    
    def calculate_metrics(self) -> None:
        self.unique_users:int = 0
        self.bounced_users:int = 0
        self.x_device_users:int = 0

        with self._lock:
            for _, metric in db.metrics.items():
                self.unique_users += 1
                self.bounced_users += 1 if metric.is_bounced() else 0
                self.x_device_users +=1 if metric.is_crossed() else 0
    
db = DB()
