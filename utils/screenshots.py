import os, time

def take_screenshot(driver, name):
    os.makedirs("artifacts/screens", exist_ok=True)
    path = os.path.join("artifacts/screens", f"{name}_{int(time.time())}.png")
    driver.save_screenshot(path)
    print(f"Screenshot saved: {path}")
    return path