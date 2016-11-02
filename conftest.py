import importlib
import json
import os.path
import pytest
import jsonpickle
from fixture.application import Application
from fixture.db import DbFixture

fixture = None
target = None


# load target.json config file
def load_config(file):
    global target
    if target is None:
        config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)  # without using Working Directory in Edit Configurations
        with open(config_file) as f:  # to open file using 'request.config.getoption('--target')' go Edit Configurations > Working Directory > choose project dir
            target = json.load(f)  # load json object to python dictionary
    return target


@pytest.fixture  # (scope='session') - one fixture for all test in session,
# example: one time  browser starts for all tests
def app(request):
    global fixture
    browser = request.config.getoption('--browser')  # config.getoption(name) to retrieve the value of a CLI option
    web_config = load_config(request.config.getoption('--target'))['web']
    if fixture is None or not fixture.is_valid():
        fixture = Application(browser=browser, base_url=web_config['baseUrl'])
    fixture.session.ensure_login(username=web_config['username'], password=web_config['password'])
    return fixture


@pytest.fixture(scope='session')
def db(request):
    db_config = load_config(request.config.getoption('--target'))['db']
    dbfixture = DbFixture(host=db_config['host'], name=db_config['name'],
                          user=db_config['user'], password=db_config['password'])

    def fin():
        dbfixture.destroy()
    request.addfinalizer(fin)
    return dbfixture


@pytest.fixture(scope='session', autouse=True)  # without autouse browser won't close
def stop(request):
    def fin():
        fixture.session.ensure_logout()
        fixture.destroy()
    request.addfinalizer(fin)  # request = parameter with method addfinalizer
    return fixture


@pytest.fixture
def check_ui(request):
    return request.config.getoption('--check_ui')


# parameters to run tests
# py.test --browser=chrome test_... to run test in different browser from CLI
# or Edit Configurations > Options > --browser=chrome
# to be able to run tests in chrome or ie you need files chromdriver and iedriverserver added to PATH
# put them in python folder for example, command "set path" in cmd
def pytest_addoption(parser):  # pytest method to hook options
    parser.addoption('--browser', action='store', default='firefox')
    parser.addoption('--target', action='store', default='target.json')
    parser.addoption('--check_ui', action='store_true')

# module to load testdata from data package
def pytest_generate_tests(metafunc):
    for fixture in metafunc.fixturenames:
        if fixture.startswith("data_"):
            testdata = load_from_module(fixture[5:])  # cut first 5 letters 'data_'
            metafunc.parametrize(fixture, testdata, ids=[str(x) for x in testdata])
        elif fixture.startswith("json_"):
            testdata = load_from_json(fixture[5:])
            metafunc.parametrize(fixture, testdata, ids=[str(x) for x in testdata])


def load_from_module(module):
    return importlib.import_module('data.%s' % module).testdata


def load_from_json(file):
    # find path of json file from data folder relatively current file path, open json file
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data/%s.json' % file)) as f:
        return jsonpickle.decode(f.read())


# fixture for web application = browser with driver from which we can
# interact with test system

# fixture when working with db = connection with db,
# we establish it and it's ready fo querying
