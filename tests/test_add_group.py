# -*- coding: utf-8 -*-
import random
import string
import pytest
from model.group import Group


# generator of random strings, maxlen var for passing to function max string len
def random_string(prefix, maxlen):
    symbols = string.ascii_letters + string.digits + string.punctuation + ' ' * 10  # + 10 whitespaces
    return prefix + ''.join([random.choice(symbols) for i in range(random.randrange(maxlen))])


# 8 groups as a result, for every parameter in Group we loop through empty or random value
# '','',''
# '','',footer
# '',header,''
# '',header,footer
# name,'',''
# name,'',footer
# name,header,''
# name,header,footer

# testdata = [
#     Group(name=name, header=header, footer=footer)
#     for name in ['', random_string('name', 10)]
#     for header in ['', random_string('header', 10)]
#     for footer in ['', random_string('footer', 10)]
# ]


#one group with empty strings and 5 random test_data strings
testdata = [Group(name='', header='', footer='')] + [
    Group(name=random_string('name', 10), header=random_string('header', 20), footer=random_string('footer', 20))
    for i in range(5)
]

# testdata = [
#     Group(name=random_string('name', 10), header=random_string('header', 20), footer=random_string('footer', 20)),
#     Group(name='', header='', footer='')
# ]


@pytest.mark.parametrize('group', testdata, ids=[repr(x) for x in testdata])  # DDT approach
# parameter isd is for list representation on test_data as text
def test_add_group(app, group):
    old_groups = app.group.get_group_list()  # get the list of groups on page before test
    app.group.create(group)  # test
    assert len(old_groups) + 1 == app.group.count()
    new_groups = app.group.get_group_list()  # get the list of groups on page after test
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
