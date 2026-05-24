from app.models.internal.interaction import Interaction
from app.models.internal.user import User
from app.models.internal.metrics import Metric
from app.models.commons.values import Source, Event

class DB:
    def __init__(self):
        self.interactions: dict[str, Interaction] = {}
        self.users: dict[str, User] = {}
        self.user_interaction: dict[str, list[str]] = {}
        self.metrics: dict[str, Metric] = {}

    def user_exist(self, user_id) -> bool:
        return user_id in self.users

    def add_user(
        self, user_id: str, parent: User | None, users_gp: set[User]
    ) -> User:
        user = User(parent, user_id, users_gp)
        self.users[user_id] = user
        return user
    
    def get_user(self, user_id: str):
        return self.users[user_id]

    def get_parent(self, user_id) -> User:
        current: str = user_id
        parent: User = self.users[current].parent

        while parent.uid != current:
            current = parent.uid
            parent = self.users[current].parent

        self.users[current].parent = parent
        return parent
    
    def add_interaction(self, iuid: str, uids: list[str], source:str, event:str) -> None:
        self.interactions[iuid] = Interaction(uids, Source(source) , Event(event))

    def add_user_interaction(self, user_id: str, interaction_id: str):
        if user_id in db.user_interaction:
            db.user_interaction[user_id].append(interaction_id)
        else:
            db.user_interaction[user_id] = [interaction_id]

db = DB()
