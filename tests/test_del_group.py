from model.group import Group


# check if there is a group before deleting
def test_delete_first_group(app):
    if not app.group.count():  # if not app.group.count(): = if not app.group.count() == False
        app.group.create(Group(name="g3"))
    app.group.delete_first_group()

