import os, time

def take_screenshot(driver, name="screenshot"):
    folder = "artifacts/screenshots"
    os.makedirs(folder, exist_ok=True)
    stamp = time.strftime("%Y%m%d_%H%M%S")
    path = f"{folder}/{name}_{stamp}.png"
    driver.save_screenshot(path)
    print(f"[screenshot] {path}")
    return path