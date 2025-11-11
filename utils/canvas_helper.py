import time, os
from selenium.webdriver.common.by import By

PANEL_SELECTOR = "app-details"
BACK_BTN = "[id='Go back to Node Config Panel']"

def panel_visible(driver):
    try:
        el = driver.find_element(By.CSS_SELECTOR, PANEL_SELECTOR)
        return el.is_displayed()
    except:
        return False

def click_back(driver, wait=None):
    try:
        btn = driver.find_element(By.CSS_SELECTOR, BACK_BTN)
        btn.click()
        time.sleep(0.4)
    except:
        pass

def cdp_click_at(driver, x, y):
    driver.execute_cdp_cmd("Input.dispatchMouseEvent", {"type":"mouseMoved","x":float(x),"y":float(y),"buttons":1})
    driver.execute_cdp_cmd("Input.dispatchMouseEvent", {"type":"mousePressed","x":float(x),"y":float(y),"button":"left","buttons":1,"clickCount":1})
    driver.execute_cdp_cmd("Input.dispatchMouseEvent", {"type":"mouseReleased","x":float(x),"y":float(y),"button":"left","buttons":1,"clickCount":1})

def get_canvas(driver):
    return driver.find_element(By.CSS_SELECTOR, "canvas")

def get_canvas_rect(driver, canvas):
    return driver.execute_script("""
      const r = arguments[0].getBoundingClientRect();
      return {left:r.left, top:r.top, w:r.width, h:r.height};
    """, canvas)

def capture_panel_screenshots(driver, count=2):
    os.makedirs("artifacts/screenshots", exist_ok=True)
    shots = 0
    for i in range(count):
        path = f"artifacts/screenshots/dot_{i+1}.png"
        driver.save_screenshot(path)
        shots += 1
    return shots