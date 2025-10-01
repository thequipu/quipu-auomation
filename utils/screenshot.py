import os
import time

def take_screenshot(driver, name="screenshot"):
    """Save a PNG screenshot to ./screenshots with a timestamped filename."""
    folder = "screenshots"
    os.makedirs(folder, exist_ok=True)
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    path = os.path.join(folder, f"{name}_{timestamp}.png")
    driver.save_screenshot(path)
    print(f"✅ Screenshot saved: {path}")
    return path