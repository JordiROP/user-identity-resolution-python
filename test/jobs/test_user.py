from app.models.internal.user import User

def test_traverse():
    u1 = User(None, "u1", set())

    u2 = User(u1, "u2", set())
    u3 = User(u1, "u3", set())

    u4 = User(u2, "u4", set())
    u5 = User(u2, "u5", set())

    u6 = User(u3, "u6", set())

    u1.intr_grp.update({u1, u2, u3})
    u2.intr_grp.update({u2, u4, u5})
    u3.intr_grp.update({u3, u6})
    u4.intr_grp.update({u4})
    u5.intr_grp.update({u5})
    u6.intr_grp.update({u6})

    expected_traversed = set(["u1", "u2", "u3", "u4", "u5", "u6"])
    traversed = u1.traverse()

    assert traversed == expected_traversed