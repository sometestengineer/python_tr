from model.group import Group
from timeit import timeit


# #  test to show time needed to execute through db and UI
# def test_group_list(app, db):
#     print timeit(lambda: app.group.get_group_list(), number=1)
#
#     def clean(group):
#         # strip spaces in names loaded from db to compare them with names loaded from UI,
#         # where spaces in the end and beginning of linea are stripped
#         return Group(id=group.id, name=group.name.strip())
#
#     print timeit(lambda: map(clean, db.get_group_list()), number=1)
#     assert False  # sorted(ui_list, key=Group.id_or_max) == sorted(db_list, key=Group.id_or_max)


def test_group_list(app, db):
    ui_list = app.group.get_group_list()
    def clean(group):
        # strip spaces in names loaded from db to compare them with names loaded from UI,
        # where spaces in the end and beginning of line are stripped
        return Group(id=group.id, name=group.name.strip())
    db_list = map(clean, db.get_group_list())
    assert sorted(ui_list, key=Group.id_or_max) == sorted(db_list, key=Group.id_or_max)
