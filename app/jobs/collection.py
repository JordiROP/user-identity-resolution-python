from app.db import db
from app.models.input.interaction import CollectInteraction

def resolve_user(reference: str):
    if not db.user_exist(reference):
        parent = db.add_user(reference, None, set())
    else:
        parent = db.get_parent(reference)
    current = db.get_user(reference)
    return parent, current

def collect(interaction: CollectInteraction):
    db.add_interaction(interaction.id_, 
                       interaction.user_ids,
                       interaction.source,
                       interaction.event)

    reference = interaction.user_ids[0]
    parent, curr_ref = resolve_user(reference)
    curr_ref.intr_grp.add(curr_ref)
    present_users = {curr_ref}
    db.add_user_interaction(reference, interaction.id_)
    
    for i in range(1, len(interaction.user_ids)):
        user_id = interaction.user_ids[i]
        db.add_user_interaction(user_id, interaction.id_)
        curr_parent, current = resolve_user(user_id)
        present_users.add(current)
        if parent.uid != curr_parent.uid:
            curr_ref.intr_grp.add(current)
            curr_parent.parent = parent
    
    for user_id in interaction.user_ids:
        db.users[user_id].intr_grp.update(present_users)
