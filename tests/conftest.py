def pytest_addoption(parser):
    parser.addoption("--host", default=None, type=str, help="run tests against remote host")


def pytest_generate_tests(metafunc):
    if 'client' in metafunc.fixturenames:
        host = metafunc.config.getoption('host')
        metafunc.parametrize('client', [host], indirect=True)
