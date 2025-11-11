import pytest
from drivers.driver_factory import DriverFactory

@pytest.fixture(scope="session")
def config():
    return DriverFactory.load_config()

@pytest.fixture(scope="function")
def driver(config):
    driver = DriverFactory.get_driver(config)
    yield driver
    driver.quit()