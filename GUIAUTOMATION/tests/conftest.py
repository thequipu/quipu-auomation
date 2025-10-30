import pytest
from drivers.driver_factory import DriverFactory
from utils.screenshots import take_screenshot

@pytest.fixture(scope="session")
def config():
    return DriverFactory.load_config()  # robust finder

@pytest.fixture(scope="function")
def driver(config, request):
    driver, wait = DriverFactory.get_driver()
    yield driver
    # screenshot-on-failure
    failed = hasattr(request.node, "rep_call") and request.node.rep_call.failed
    if failed:
        take_screenshot(driver, f"FAILED_{request.node.name}")
    driver.quit()

# hook to know test status (for screenshot-on-failure)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)