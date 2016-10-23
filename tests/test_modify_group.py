from model.group import Group
from random import randrange


def test_modify_group_name(app):
    if app.group.count() == 0:  # precondition
        app.group.create(Group(name="g3"))
    old_groups = app.group.get_group_list()
    index = randrange(len(old_groups))  # index = number of group on group page
    print 'index %s' % index
    group = Group(name='New group')
    group.id = old_groups[index].id  # remember id of a group, id from web page
    app.group.modify_group_by_index(index, group)  # test
    new_groups = app.group.get_group_list()
    assert len(old_groups) == len(new_groups)
    old_groups[index] = group
    assert sorted(old_groups, key=Group.id_or_max) == sorted(new_groups, key=Group.id_or_max)


# def test_modify_group_header(app):
#     old_groups = app.group.get_group_list()
#     app.group.modify_first_group(Group(header='New header'))
#     new_group = app.group.get_group_list()
#     assert len(old_groups) == len(new_group)
