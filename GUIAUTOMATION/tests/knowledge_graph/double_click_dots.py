import os, time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# -------------------- setup + login --------------------
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 20)

driver.get("http://localhost:4200/login")
driver.maximize_window()

wait.until(EC.presence_of_element_located((By.ID, "tenantId"))).send_keys("preprodquipuai1")
wait.until(EC.element_to_be_clickable((By.ID, "tenant-btn"))).click()
wait.until(EC.presence_of_element_located((By.ID, "username"))).send_keys("narenm")
wait.until(EC.presence_of_element_located((By.ID, "password"))).send_keys("12!Quipu345")
wait.until(EC.element_to_be_clickable((By.ID, "signIn-btn"))).click()

# -------------------- navigate to KG --------------------
wait.until(EC.element_to_be_clickable((By.ID, "page-menu"))).click(); time.sleep(2)
wait.until(EC.element_to_be_clickable((By.ID, "Knowledge Graph-page"))).click(); time.sleep(2)
wait.until(EC.presence_of_element_located((By.ID, "fabric-menu"))).click(); time.sleep(2)
wait.until(EC.presence_of_element_located((By.ID, "RealWorldDataMart-fabric"))).click(); time.sleep(2)

wait.until(EC.element_to_be_clickable((By.ID, "label-address"))).click()
time.sleep(3)

# -------------------- helpers --------------------
PANEL_SELECTOR = "app-details, app-node-info, .left-container"

def panel_visible():
    try:
        els = driver.find_elements(By.CSS_SELECTOR, PANEL_SELECTOR)
        return any(e.is_displayed() for e in els)
    except:
        return False

def cdp_click_at(cx, cy, clicks=1):
    """send real mouse events at given coords; clicks=2 → double-click"""
    driver.execute_cdp_cmd("Input.dispatchMouseEvent",
                           {"type": "mouseMoved", "x": float(cx), "y": float(cy), "buttons": 1})
    driver.execute_cdp_cmd("Input.dispatchMouseEvent",
                           {"type": "mousePressed", "x": float(cx), "y": float(cy),
                            "button": "left", "buttons": 1, "clickCount": clicks})
    driver.execute_cdp_cmd("Input.dispatchMouseEvent",
                           {"type": "mouseReleased", "x": float(cx), "y": float(cy),
                            "button": "left", "buttons": 1, "clickCount": clicks})

# -------------------- canvas --------------------
canvas = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "canvas")))
driver.execute_script("arguments[0].scrollIntoView({block:'center', inline:'center'});", canvas)
time.sleep(0.3)

os.makedirs("artifacts/screens", exist_ok=True)

rect = driver.execute_script("""
  const r = arguments[0].getBoundingClientRect();
  return {left:r.left + window.scrollX, top:r.top + window.scrollY, w:r.width, h:r.height};
""", canvas)

# -------------------- scan for a node --------------------
clicked_px = None
step = 80
sx, ex = int(rect["left"]+200), int(rect["left"]+rect["w"]-20)
sy, ey = int(rect["top"]+40), int(rect["top"]+rect["h"]-40)

found = False
y = sy
while y < ey and not found:
    x = sx
    while x < ex and not found:
        print(f"scan click @ ({x},{y})")
        cdp_click_at(x, y, clicks=1)

        end = time.time() + 6
        while time.time() < end and not panel_visible():
            time.sleep(0.1)

        if panel_visible():
            clicked_px = (x, y)
            out1 = "artifacts/screens/panel_after_click.png"
            driver.save_screenshot(out1)
            print("panel screenshot:", out1)
            found = True
            break
        x += step
    y += step

if not found:
    print("No panel found.")
    driver.quit()
    raise SystemExit(0)

# -------------------- double-click same coords --------------------
print(f"double-click same node @ {clicked_px}")
cdp_click_at(clicked_px[0], clicked_px[1], clicks=2)

time.sleep(5)  # wait for graph to change
out2 = "artifacts/screens/after_doubleclick_next_graph.png"
driver.save_screenshot(out2)
print("next graph screenshot:", out2)

time.sleep(10)
driver.quit()