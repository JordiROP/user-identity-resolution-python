from app.jobs.collection import process_collect
from app.jobs.update import process_update
from app.jobs.metrics import process_metrics
from app.db import db

from app.models.input.interaction import CollectInteraction, UpdateInteraction

import pytest


@pytest.fixture(autouse=True)
def clean_db():
    db.interactions = {}
    db.users = {}
    db.user_interaction = {}
    db.metrics = {}

def test_process_metrics():
    inputs = [
        {"id":"ded25add-bf08-4eda-a32f-a0e7424a9369","userIds":["u1"],"source":"appscreen","event":"display"},
        {"id":"cbe83fdc-4b5c-4728-9db4-bcb269f5a2e0","userIds":["u2","u22","u31","u32"],"source":"webpage","event":"display"},
        {"id":"7c51900e-bb98-422c-a830-35ff0e00b8e4","userIds":["u32","u33"],"source":"appscreen","event":"buy"},
        {"id":"1ae20cbb-e1bd-4843-b787-f71707c7dd6e","userIds":["u4"],"source":"webpage","event":"buy"},
        {"id":"cbe83fdc-4b5c-4728-9db4-bcb269f5a2e1","userIds":["u5"], "source":"appscreen","event":"display"},
        {"id":"0067fd88-511e-48bf-a944-cc743bd01f03","userIds":["u5","u51","u52"],"source":"appscreen","event":"buy"},
        {"id":"565594d0-2c2e-40ed-9b1d-3f0e1a7f2eeb","userIds":["u6","u61","u62"],"source":"webpage","event":"display"},
        {"id":"7fbcedc3-d47d-4aaa-9616-4b847519690c","userIds":["u7","u71","u72"],"source":"appscreen","event":"display"}]
    
    for input in inputs:
        process_collect(CollectInteraction(**input))
    
    expected_metrics = {
                        "uniqueUsers": 6,
                        "bouncedUsers": 3,
                        "crossDeviceUsers": 1
                    }

    metrics = process_metrics()
    assert metrics == expected_metrics

def test_process_metrics_after_update():
    inputs = [
        {"id":"ded25add-bf08-4eda-a32f-a0e7424a9369","userIds":["u1"],"source":"appscreen","event":"display"},
        {"id":"cbe83fdc-4b5c-4728-9db4-bcb269f5a2e0","userIds":["u2","u22","u31","u32"],"source":"webpage","event":"display"},
        {"id":"7c51900e-bb98-422c-a830-35ff0e00b8e4","userIds":["u32","u33"],"source":"appscreen","event":"buy"},
        {"id":"1ae20cbb-e1bd-4843-b787-f71707c7dd6e","userIds":["u4"],"source":"webpage","event":"buy"},
        {"id":"cbe83fdc-4b5c-4728-9db4-bcb269f5a2e1","userIds":["u5"], "source":"appscreen","event":"display"},
        {"id":"0067fd88-511e-48bf-a944-cc743bd01f03","userIds":["u5","u51","u52"],"source":"appscreen","event":"buy"},
        {"id":"565594d0-2c2e-40ed-9b1d-3f0e1a7f2eeb","userIds":["u6","u61","u62"],"source":"webpage","event":"display"},
        {"id":"7fbcedc3-d47d-4aaa-9616-4b847519690c","userIds":["u7","u71","u72"],"source":"appscreen","event":"display"}]
    
    updates = [
        {"id":"7c51900e-bb98-422c-a830-35ff0e00b8e4","userIds":["u32","u33", "u62"]},
        {"id":"0067fd88-511e-48bf-a944-cc743bd01f03","userIds":["u51","u52"]},
        {"id":"7fbcedc3-d47d-4aaa-9616-4b847519690c","userIds":["u7","u6"]}]

    for input in inputs:
        process_collect(CollectInteraction(**input))
    
    for update in updates:
        process_update(UpdateInteraction(**update))
    
    expected_metrics = {
                        "uniqueUsers": 5,
                        "bouncedUsers": 2,
                        "crossDeviceUsers": 1
                    }

    metrics = process_metrics()
    assert metrics == expected_metrics