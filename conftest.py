import pytest
from fixture.application import Application


fixture = None


@pytest.fixture  # (scope='session') - one fixture for all test in session,
# example: one time browser starts for all tests
def app(request):
    global fixture
    if fixture is None:
        fixture = Application()
        fixture.session.login(username="admin", password="secret")
    else:
        if not fixture.is_valid():
            fixture = Application()
            fixture.session.login(username="admin", password="secret")
    # fixture.session.ensure_login(username="admin", password="secret")
    return fixture


@pytest.fixture(scope='session', autouse=True)  # without autouse browser won't close
def stop(request):
    def fin():
        # fixture.session.ensure_logout()
        fixture.session.logout()
        fixture.destroy()
    request.addfinalizer(fin)  # request = parameter with method addfinalizer
    return fixture


# fixture for web application = browser with driver from which we can
# interact with test system

# fixture when working with db = connection with db,
# we establish it and it's ready fo querying
