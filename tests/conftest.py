def pytest_addoption(parser):
    parser.addoption("--prod", action="store_true", help="run tests against prod")


def pytest_generate_tests(metafunc):
    if 'client' in metafunc.fixturenames:
        if metafunc.config.getoption('prod'):
            target = 'prod'
        else:
            target = 'local'
        metafunc.parametrize('client', [target], indirect=True)
