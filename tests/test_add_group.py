# -*- coding: utf-8 -*-
import pytest

from fixture.application import Application
from model.group import Group


@pytest.fixture
def app(request):
    fixture = Application()
    request.addfinalizer(fixture.destroy)  # request = parameter with method addfinalizer
    return fixture


def test_add_group(app):
    app.session.login(username="admin", password="secret")
    app.group.create(Group(name="g3", header="g3", footer="g33"))
    app.session.logout()


def test_add_empty_group(app):
    app.session.login(username="admin", password="secret")
    app.group.create(Group(name="", header="", footer=""))
    app.session.logout()
