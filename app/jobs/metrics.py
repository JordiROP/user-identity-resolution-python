from app.db import db


def process_metrics():
    unique_users:int = 0
    bounced_users:int = 0
    x_device_users:int = 0

    for _, metric in db.metrics.items():
