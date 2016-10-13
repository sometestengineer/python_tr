import pytest
from fixture.application import Application


@pytest.fixture(scope='session')  # scope='session' - one fixture for all test in session,
# example: one time browser starts for all tests
def app(request):
    fixture = Application()
    request.addfinalizer(fixture.destroy)  # request = parameter with method addfinalizer
    return fixture
