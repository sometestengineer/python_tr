# -*- coding: utf-8 -*-
from model.group import Group
# import pytest
# from data.groups import constant as testdata


# @pytest.mark.parametrize('group', testdata, ids=[repr(x) for x in testdata])  # DDT approach
# parameter isd is for list representation on test_data as text
def test_add_group(app, db, json_groups):  # data_groups to use data/groups.py
    group = json_groups
    old_groups = db.get_group_list()  # get the list of groups in db before test
    app.group.create(group)  # test
    new_groups = db.get_group_list()  # get the list of groups in db after test
    old_groups.append(group)
    assert sorted(old_groups, key=Group.id_or_max) == sorted(new_groups, key=Group.id_or_max)


# def test_add_empty_group(app):
#     old_groups = app.group.get_group_list()
#     group = Group(name="", header="", footer="")
#     app.group.create(group)
#     new_groups = app.group.get_group_list()
#     assert len(old_groups) + 1 == len(new_groups)
#     old_groups.append(group)
#     assert sorted(old_groups, key=Group.id_or_max) == sorted(new_groups, key=Group.id_or_max)
