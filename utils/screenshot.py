import os, time

def take_screenshot(driver, name="screenshot"):
    folder = "artifacts/screenshots"
    os.makedirs(folder, exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    path = f"{folder}/{name}_{timestamp}.png"
    driver.save_screenshot(path)
    print(f"Screenshot saved: {path}")
    return path