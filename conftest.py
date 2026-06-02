def pytest_addoption(parser):
    parser.addoption("--base-url", default=None, type=str, help="change the base url")


def pytest_generate_tests(metafunc):
    if 'client' in metafunc.fixturenames:
        base_url = metafunc.config.getoption('base_url')
        metafunc.parametrize('client', [base_url], indirect=True)
