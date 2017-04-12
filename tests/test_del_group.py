from model.group import Group
import random


# check if there is a group before deleting
def test_delete_some_group(app, db, check_ui):
    if len(db.get_group_list()) == 0:
        app.group.create(Group(name="g3"))
    old_groups = db.get_group_list()
    group = random.choice(old_groups)
    app.group.delete_group_by_id(group.id)  # delete group passing group number
    print 'id = %s' % group.id
    new_groups = db.get_group_list()
    assert len(old_groups) - 1 == len(new_groups)  # will catch error if group list is empty, with clearer diagnostics
    old_groups.remove(group)
    assert old_groups == new_groups
    # optional check in UI, not through db
    if check_ui:
        assert sorted(new_groups, key=Group.id_or_max) == sorted(app.group.get_group_list(), key=Group.id_or_max)

# # check if there is a group before deleting
# def test_delete_some_group(app, db):
#     if app.group.count() == 0:  # if not app.group.count(): = if not app.group.count() == False
#         app.group.create(Group(name="g3"))
#     old_groups = app.group.get_group_list()
#     # chooses random group, if there is no it crashes
#     index = randrange(len(old_groups))
#     print 'index %s' % index
#     app.group.delete_group_by_index(index)  # delete group passing group number
#     new_groups = app.group.get_group_list()
#     assert len(old_groups) - 1 == len(new_groups)
#     old_groups[index:index+1] = []  # del index element in list, [0:1] = first element
#     assert old_groups == new_groups
