from app.models.internal.interaction import Interaction
from app.models.internal.user import User
from app.models.internal.metrics import Metric

class DB:
    def __init__(self):
        self.interactions: dict[str, Interaction] = {}
        self.users: dict[str, User] = {}
        self.user_interaction: dict[str, str] = {}
        self.metrics: dict[str, Metric] = {} 

    def user_exist(self, user_id) -> bool:
        return user_id in self.users
    
    def create_user(self, user_id: str, parent:str, users_gp: list[str]) -> None:
        self.users[user_id] = User(parent, users_gp)

    def get_parent(self, user_id):
        current:str = user_id
        parent:str = self.users[current].parent
        
        while parent != current:
            current = parent 
            parent = self.users[current].parent
        
        self.users[current].parent = parent
        return parent
        

db = DB()