from app.db import db
from models.input.interaction import CollectInteraction

def collect(interaction: CollectInteraction):
    parent = interaction.user_ids[0]
    

