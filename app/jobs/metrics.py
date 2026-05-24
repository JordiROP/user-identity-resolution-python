from app.db import db


def process_metrics():
    unique_users:int = 0
    bounced_users:int = 0
    x_device_users:int = 0

    for _, metric in db.metrics.items():
        unique_users += 1
        bounced_users += 1 if len(metric.event) == 0 else 0