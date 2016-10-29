import json
import os.path
import pytest
from fixture.application import Application


fixture = None
target = None


@pytest.fixture  # (scope='session') - one fixture for all test in session,
# example: one time browser starts for all tests
def app(request):
    global fixture
    global target
    browser = request.config.getoption('--browser')  # config.getoption(name) to retrieve the value of a CLI option
    if target is None:
        config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), request.config.getoption('--target'))  # without using Working Directory in Edit Configurations
        with open(config_file) as f:  # to open file using 'request.config.getoption('--target')' go Edit Configurations > Working Directory > choose project dir
            target = json.load(f)  # load json object to python dictionary
    if fixture is None or not fixture.is_valid():
        fixture = Application(browser=browser, base_url=target['baseUrl'])
    fixture.session.ensure_login(username=target['username'], password=target['password'])
    return fixture


@pytest.fixture(scope='session', autouse=True)  # without autouse browser won't close
def stop(request):
    def fin():
        fixture.session.ensure_logout()
        fixture.destroy()
    request.addfinalizer(fin)  # request = parameter with method addfinalizer
    return fixture


# parameters to run tests
# py.test --browser=chrome test_... to run test in different browser from CLI
# or Edit Configurations > Options > --browser=chrome
# to be able to run tests in chrome or ie you need files chromdriver and iedriverserver added to PATH
# put them in python folder for example, command "set path" in cmd
def pytest_addoption(parser):  # pytest method to hook options
    parser.addoption('--browser', action='store', default='firefox')
    parser.addoption('--target', action='store', default='target.json')


# fixture for web application = browser with driver from which we can
# interact with test system

# fixture when working with db = connection with db,
# we establish it and it's ready fo querying
