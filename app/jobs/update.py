from app.db import db
from app.models.internal.user import User
from app.models.internal.interaction import Interaction
from app.models.input.interaction import UpdateInteraction

def get_existing_new_users(up_users: set[str], current_intr_users: set[str]) -> tuple[set[str], set[str], set[str]]:
    new_users: set[str] = set()
    outsiders: set[str] = set()
    insiders: set[str] = set()

    for user in up_users:
        if db.user_exist(user):
            if user not in current_intr_users:
                outsiders.add(user)
            else:
                insiders.add(user)
        else:
            new_users.add(user)
    
    return new_users, outsiders, insiders

def process_new_users(interaction_id: str, current_intr: Interaction, 
                           new_users: set[str], ref_parent: User, 
                           up_users: set[str]) -> None:
    intr_users: set[User] = {db.get_user(uid) for uid in up_users if uid in db.users}
    
    current_intr.user_ids.update(new_users)
    for user in new_users:
        db.add_user_interaction(user, interaction_id)
        db.add_user(user, ref_parent, intr_users)
    
    created_users: set[User] = {db.get_user(uid) for uid in new_users}
    for user in created_users.union(intr_users):
        db.update_usr_intr_grp(user.uid, created_users)
    
    db.update_users_interaction(interaction_id, up_users)

def process_merge_users(current_intr: Interaction, up_users: set[str], 
                        ref_parent: User, outsiders: set[str], insiders: set[str]) -> None:
    current_intr.user_ids = up_users
    db.add_recompute(ref_parent.traverse())
    new_users = insiders.union(outsiders)
    merged_users = {db.get_user(uid) for uid in new_users}
    for user in merged_users:
        user.intr_grp.update(merged_users)
        if not db.in_recompute(user.uid):
            db.add_recompute(user.traverse())

def process_update(interaction: UpdateInteraction) -> None:
    current_intr: Interaction = db.get_interaction(interaction.id_)
    up_users: set[str] = interaction.user_ids

    removed_users: set[str] = {uid for uid in current_intr.user_ids if uid not in up_users}
    new_users, outsiders, insiders = get_existing_new_users(up_users, current_intr.user_ids)
    ref_parent = db.get_parent(next(iter(insiders)))

    if new_users:
        process_new_users(interaction.id_, current_intr, new_users, ref_parent, up_users)
    
    if outsiders:
        process_merge_users(current_intr, up_users, ref_parent, outsiders, insiders)
        
