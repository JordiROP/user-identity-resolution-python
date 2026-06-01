from app.models.input.interaction import CollectInteraction, UpdateInteraction
from app.models.internal.interaction import Interaction
from app.models.internal.user import User
from app.models.commons.values import Event, Source
from app.db import db

from app.jobs.collection import process_collect
from app.jobs.update import process_update

import pytest

@pytest.fixture(autouse=True)
def clean_db():
    db.interactions = {}
    db.users = {}
    db.user_interaction = {}
    db.metrics = {}

def test_update_new_users_only():
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
        {"id":"7c51900e-bb98-422c-a830-35ff0e00b8e4","userIds":["u32","u33","u34"]},
        {"id":"7fbcedc3-d47d-4aaa-9616-4b847519690c","userIds":["u7","u71","u72","u73"]},
    ]

    expected_traverse = {'u1': {'u1'}, 
                         'u4': {'u4'}, 
                         'u5': {'u51', 'u52', 'u5'}, 
                         'u51': {'u51', 'u52', 'u5'}, 
                         'u52': {'u51', 'u52', 'u5'}, 
                         'u6': {'u62', 'u61', 'u6'}, 
                         'u61': {'u62', 'u61', 'u6'}, 
                         'u62': {'u61', 'u6', 'u62'}, 
                         'u32': {'u33', 'u34', 'u31', 'u32', 'u2', 'u22'}, 
                         'u22': {'u34', 'u33', 'u31', 'u32', 'u2', 'u22'}, 
                         'u2': {'u34', 'u33', 'u31', 'u32', 'u2', 'u22'}, 
                         'u31': {'u34', 'u33', 'u31', 'u32', 'u2', 'u22'}, 
                         'u33': {'u33', 'u34', 'u31', 'u32', 'u2', 'u22'}, 
                         'u34': {'u34', 'u33', 'u31', 'u32', 'u2', 'u22'}, 
                         'u72': {'u72', 'u7', 'u73', 'u71'}, 
                         'u7': {'u72', 'u7', 'u73', 'u71'}, 
                         'u73': {'u72', 'u7', 'u73', 'u71'}, 
                         'u71': {'u72', 'u7', 'u73', 'u71'}}

    expected_interactions = {
        "ded25add-bf08-4eda-a32f-a0e7424a9369": Interaction({"u1"}, Source("appscreen"), Event("display")),
        "cbe83fdc-4b5c-4728-9db4-bcb269f5a2e0": Interaction({"u2","u22","u31","u32"}, Source("webpage"), Event("display")),
        "7c51900e-bb98-422c-a830-35ff0e00b8e4": Interaction({"u32","u33","u34"}, Source("appscreen"), Event("buy")),
        "1ae20cbb-e1bd-4843-b787-f71707c7dd6e": Interaction({"u4"},Source("webpage"), Event("buy")),
        "cbe83fdc-4b5c-4728-9db4-bcb269f5a2e1": Interaction({"u5"}, Source("appscreen"), Event("display")),
        "0067fd88-511e-48bf-a944-cc743bd01f03": Interaction({"u5","u51","u52"}, Source("appscreen"), Event("buy")),
        "565594d0-2c2e-40ed-9b1d-3f0e1a7f2eeb": Interaction({"u6","u61","u62"}, Source("webpage"), Event("display")),
        "7fbcedc3-d47d-4aaa-9616-4b847519690c": Interaction({"u7","u71","u72","u73"}, Source("appscreen"), Event("display"))
    }

    for inter in inputs:
        process_collect(CollectInteraction(**inter))
    
    for inter in updates:
        process_update(UpdateInteraction(**inter))

    traverses = {uid: user.traverse() for uid, user in db.users.items()}

    assert db.interactions == expected_interactions
    assert traverses == expected_traverse

def test_update_add_existing_users():
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
    ]

    exptected_traverse = {'u1': {'u1'}, 
                          'u4': {'u4'}, 
                          'u5': {'u51', 'u52', 'u5'}, 
                          'u51': {'u51', 'u52', 'u5'}, 
                          'u52': {'u51', 'u52', 'u5'}, 
                          'u7': {'u7', 'u71', 'u72'}, 
                          'u71': {'u7', 'u71', 'u72'}, 
                          'u72': {'u7', 'u71', 'u72'}, 
                          'u33': {'u2', 'u33', 'u22', 'u61', 'u62', 'u6', 'u31', 'u32'}, 
                          'u62': {'u2', 'u33', 'u22', 'u61', 'u62', 'u6', 'u31', 'u32'}, 
                          'u32': {'u2', 'u33', 'u22', 'u61', 'u62', 'u6', 'u31', 'u32'}, 
                          'u2': {'u2', 'u33', 'u22', 'u61', 'u62', 'u6', 'u31', 'u32'}, 
                          'u22': {'u2', 'u33', 'u22', 'u61', 'u62', 'u6', 'u31', 'u32'}, 
                          'u31': {'u2', 'u33', 'u22', 'u61', 'u62', 'u6', 'u31', 'u32'}, 
                          'u6': {'u2', 'u33', 'u22', 'u61', 'u62', 'u6', 'u31', 'u32'}, 
                          'u61': {'u2', 'u33', 'u22', 'u61', 'u62', 'u6', 'u31', 'u32'}}

    expected_interactions = {
        "ded25add-bf08-4eda-a32f-a0e7424a9369": Interaction({"u1"}, Source("appscreen"), Event("display")),
        "cbe83fdc-4b5c-4728-9db4-bcb269f5a2e0": Interaction({"u2","u22","u31","u32"}, Source("webpage"), Event("display")),
        "7c51900e-bb98-422c-a830-35ff0e00b8e4": Interaction({"u32","u33","u62"}, Source("appscreen"), Event("buy")),
        "1ae20cbb-e1bd-4843-b787-f71707c7dd6e": Interaction({"u4"},Source("webpage"), Event("buy")),
        "cbe83fdc-4b5c-4728-9db4-bcb269f5a2e1": Interaction({"u5"}, Source("appscreen"), Event("display")),
        "0067fd88-511e-48bf-a944-cc743bd01f03": Interaction({"u5","u51","u52"}, Source("appscreen"), Event("buy")),
        "565594d0-2c2e-40ed-9b1d-3f0e1a7f2eeb": Interaction({"u6","u61","u62"}, Source("webpage"), Event("display")),
        "7fbcedc3-d47d-4aaa-9616-4b847519690c": Interaction({"u7","u71","u72"}, Source("appscreen"), Event("display"))
    }

    for inter in inputs:
        process_collect(CollectInteraction(**inter))

    for inter in updates:
        process_update(UpdateInteraction(**inter))


    traverses = {uid: user.traverse() for uid, user in db.users.items()}

    assert db.interactions == expected_interactions
    assert traverses == exptected_traverse

def test_update_remove_users():
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
        {"id":"cbe83fdc-4b5c-4728-9db4-bcb269f5a2e0","userIds":["u2","u22","u31"]},
    ]

    expected_traverse = {'u1': {'u1'}, 
                         'u4': {'u4'}, 
                         'u5': {'u5', 'u52', 'u51'}, 
                         'u51': {'u5', 'u51', 'u52'}, 
                         'u52': {'u5', 'u52', 'u51'}, 
                         'u6': {'u61', 'u6', 'u62'}, 
                         'u61': {'u61', 'u6', 'u62'}, 
                         'u62': {'u61', 'u6', 'u62'}, 
                         'u7': {'u7', 'u72', 'u71'}, 
                         'u71': {'u7', 'u72', 'u71'}, 
                         'u72': {'u7', 'u72', 'u71'}, 
                         'u31': {'u31', 'u22', 'u2'}, 
                         'u22': {'u31', 'u22', 'u2'}, 
                         'u2': {'u31', 'u22', 'u2'}, 
                         'u33': {'u33', 'u32'}, 
                         'u32': {'u33', 'u32'}}

    expected_interactions = {
        "ded25add-bf08-4eda-a32f-a0e7424a9369": Interaction({"u1"}, Source("appscreen"), Event("display")),
        "cbe83fdc-4b5c-4728-9db4-bcb269f5a2e0": Interaction({"u2","u22","u31"}, Source("webpage"), Event("display")),
        "7c51900e-bb98-422c-a830-35ff0e00b8e4": Interaction({"u32","u33"}, Source("appscreen"), Event("buy")),
        "1ae20cbb-e1bd-4843-b787-f71707c7dd6e": Interaction({"u4"},Source("webpage"), Event("buy")),
        "cbe83fdc-4b5c-4728-9db4-bcb269f5a2e1": Interaction({"u5"}, Source("appscreen"), Event("display")),
        "0067fd88-511e-48bf-a944-cc743bd01f03": Interaction({"u5","u51","u52"}, Source("appscreen"), Event("buy")),
        "565594d0-2c2e-40ed-9b1d-3f0e1a7f2eeb": Interaction({"u6","u61","u62"}, Source("webpage"), Event("display")),
        "7fbcedc3-d47d-4aaa-9616-4b847519690c": Interaction({"u7","u71","u72"}, Source("appscreen"), Event("display"))
    }

    for inter in inputs:
        process_collect(CollectInteraction(**inter))

    for inter in updates:
        process_update(UpdateInteraction(**inter))

    traverses = {uid: user.traverse() for uid, user in db.users.items()}

    assert db.interactions == expected_interactions
    assert traverses == expected_traverse