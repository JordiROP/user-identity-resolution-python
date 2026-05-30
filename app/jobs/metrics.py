from app.db import db
from app.models.input.interaction import CollectInteraction
from app.models.internal.interaction import Interaction
from app.jobs.collection import process_collect

def process_recompute():
    interactions: set[str] = set.union(*(db.get_interaction_from_user(uid) for uid in db.recompute))
    db.clear_reacomputed_data()
    for iuid in interactions:
        current_intr: Interaction = db.get_interaction(iuid)
        process_collect(CollectInteraction(id=iuid, source=current_intr.source, event=current_intr.event, userIds=list(current_intr.user_ids)))
    db.restart_recompute()


def get_metrics_counter():
    unique_users:int = 0
    bounced_users:int = 0
    x_device_users:int = 0

    for _, metric in db.metrics.items():
        unique_users += 1
        bounced_users += 1 if metric.is_bounced() else 0
        x_device_users +=1 if metric.is_crossed() else 0
    
    return unique_users, bounced_users, x_device_users

def process_metrics():
    if db.recompute:
        process_recompute()

    unique_users, bounced_users, x_device_users = get_metrics_counter()
    
    return {
            "uniqueUsers": unique_users,
            "bouncedUsers" : bounced_users,
            "crossDeviceUsers" : x_device_users
        }