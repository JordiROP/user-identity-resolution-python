from app.db import db


def process_metrics():
    unique_users:int = 0
    bounced_users:int = 0
    x_device_users:int = 0

    for _, metric in db.metrics.items():
        unique_users += 1
        bounced_users += 1 if metric.is_bounced() else 0
        x_device_users +=1 if metric.is_crossed() else 0
    
    return {
            "uniqueUsers": unique_users,
            "bouncedUsers" : bounced_users,
            "crossDeviceUsers" : x_device_users
        }