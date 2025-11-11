# tests/conftest.py
import os
from datetime import datetime
import pytest
from drivers.driver_factory import DriverFactory

@pytest.fixture(scope="session")
def config():
    return DriverFactory.load_config()

@pytest.fixture(scope="function")
def driver(config, request):
    drv = DriverFactory.get_driver(config)
    yield drv

    # Was the test call phase marked failed?
    rep = getattr(request.node, "rep_call", None)
    failed = bool(rep and getattr(rep, "failed", False))

    # On failure, save a screenshot
    if failed:
        os.makedirs("artifacts/screens", exist_ok=True)
        ts = int(datetime.now().timestamp())
        path = f"artifacts/screens/FAILED_{request.node.name}_{ts}.png"
        try:
            drv.save_screenshot(path)
            print(f"Screenshot saved: {path}")
        except Exception:
            pass

    drv.quit()

# --- This hook populates item.rep_setup / item.rep_call / item.rep_teardown
@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)