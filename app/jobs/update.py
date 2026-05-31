from app.db import db
from app.models.internal.interaction import Interaction
from app.models.input.interaction import UpdateInteraction, CollectInteraction

from app.jobs.collection import process_collect

def process_update(interaction: UpdateInteraction) -> None:
    original_intr: Interaction = db.get_interaction(interaction.id_)
    original_usrs: set[str] = original_intr.user_ids
    updated_usrs: set[str] = interaction.user_ids
    to_visit: set[str] = original_usrs.union(updated_usrs)
    visited: set[str] = set()
    recompute: set[str] = set()

    while to_visit:
        uid = to_visit.pop()
        if db.user_exist(uid) and uid not in visited:
            visited.update(db.get_user(uid).traverse())
            
    for uid in visited:
        recompute.update(db.get_interaction_from_user(uid))
        db.delete_user(uid)
    
    db.update_users_interaction(interaction.id_, updated_usrs)
    
    for iid in recompute:
        repr_intr: Interaction = db.get_interaction(iid)
        process_collect(CollectInteraction(id=iid, source=repr_intr.source, event=repr_intr.event, userIds=list(repr_intr.user_ids)))
    
    db.calculate_metrics()