from app.db import db
from app.models.internal.user import User
from app.models.input.interaction import CollectInteraction

def resolve_user(reference: str) -> tuple[User, User]:
    if not db.user_exist(reference):
        parent = db.add_user(reference, None, set())
    else:
        parent = db.get_parent(reference)
    current = db.get_user(reference)
    return parent, current

def process_collect(interaction: CollectInteraction) -> None:
    db.add_interaction(interaction.id_, 
                       set(interaction.user_ids),
                       interaction.source,
                       interaction.event)

    reference = interaction.user_ids[0]
    parent, curr_ref = resolve_user(reference)
    curr_ref.intr_grp.add(curr_ref)
    present_users = {curr_ref}
    db.add_user_interaction(reference, interaction.id_)

    if db.has_metrics(parent.uid):
        metric = db.get_metric(parent.uid)
        metric.update_metric(interaction.source, interaction.event)
    else:
        metric = db.create_metric(parent.uid, interaction.source, interaction.event)
    
    for i in range(1, len(interaction.user_ids)):
        user_id = interaction.user_ids[i]
        db.add_user_interaction(user_id, interaction.id_)
        curr_parent, current = resolve_user(user_id)
        present_users.add(current)
        if parent.uid != curr_parent.uid:
            curr_ref.intr_grp.add(current)
            curr_parent.parent = parent
            if db.has_metrics(curr_parent.uid):
                curr_parent_metric = db.get_metric(curr_parent.uid)
                metric.merge_metrics(curr_parent_metric)
                db.delete_metric(curr_parent.uid)
    
    for user_id in interaction.user_ids:
        db.users[user_id].intr_grp.update(present_users)
