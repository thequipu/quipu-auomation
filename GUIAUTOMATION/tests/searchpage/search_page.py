import os, time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# -------------------- setup + login --------------------
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 20)

driver.get("https://app-preprod-1.thequipu.in/")
driver.maximize_window()

tenant_input = wait.until(EC.presence_of_element_located((By.ID, "tenantId")))
tenant_input.send_keys("preprodquipuai1"); time.sleep(1)
wait.until(EC.element_to_be_clickable((By.ID, "tenant-btn"))).click()

wait.until(EC.presence_of_element_located((By.ID, "username"))).send_keys("narenm")
wait.until(EC.presence_of_element_located((By.ID, "password"))).send_keys("12!Quipu345")
wait.until(EC.element_to_be_clickable((By.ID, "signIn-btn"))).click()

wait.until(EC.presence_of_element_located((By.ID, "fabric-menu"))).click(); time.sleep(2)
wait.until(EC.presence_of_element_located((By.ID, "RealWorldDataMart-fabric"))).click(); time.sleep(2)

# --------------- search page ----------------------
search_input = wait.until(EC.presence_of_element_located((By.ID, "search-query")))
search_input.send_keys("liam Gurret")
search_input.send_keys(Keys.ENTER)
time.sleep(5)

# -------------------- helpers --------------------
PANEL_SELECTOR = "app-details, app-node-info, .left-container"
CLOSE_PANEL_ID = "#Go\\ back\\ to\\ Node\\ Config\\ Panel"   # exact id (spaces escaped)

def panel_visible():
    try:
        els = driver.find_elements(By.CSS_SELECTOR, PANEL_SELECTOR)
        return any(e.is_displayed() for e in els)
    except:
        return False

def cdp_click_at(cx, cy, clicks=1):
    driver.execute_cdp_cmd("Input.dispatchMouseEvent",
        {"type":"mouseMoved","x":float(cx),"y":float(cy),"buttons":1})
    driver.execute_cdp_cmd("Input.dispatchMouseEvent",
        {"type":"mousePressed","x":float(cx),"y":float(cy),
         "button":"left","buttons":1,"clickCount":clicks})
    driver.execute_cdp_cmd("Input.dispatchMouseEvent",
        {"type":"mouseReleased","x":float(cx),"y":float(cy),
         "button":"left","buttons":1,"clickCount":clicks})

def close_panel_if_open(timeout=5):
    if not panel_visible():
        return
    try:
        btn = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, CLOSE_PANEL_ID))
        )
        btn.click()
        WebDriverWait(driver, timeout).until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, PANEL_SELECTOR))
        )
        print("panel closed via Go back to Node Config Panel")
    except Exception as e:
        print("close panel failed:", e)

# -------------------- canvas --------------------
canvas = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "canvas")))
driver.execute_script("arguments[0].scrollIntoView({block:'center', inline:'center'});", canvas)
time.sleep(0.5)

os.makedirs("artifacts/screens", exist_ok=True)

# canvas rect in PAGE coords (with scroll)
rect = driver.execute_script("""
  const r = arguments[0].getBoundingClientRect();
  return {left:r.left + window.scrollX, top:r.top + window.scrollY, w:r.width, h:r.height};
""", canvas)

# -------------------- center-first probe (fast) --------------------
clicked_px = None

cx = rect["left"] + (rect["w"] / 2.0)
cy = rect["top"]  + (rect["h"] / 2.0)

probes = [
    (int(cx), int(cy)),
    (int(cx), int(cy - 30)),
    (int(cx + 30), int(cy)),
    (int(cx - 30), int(cy)),
    (int(cx), int(cy + 30)),
    (int(cx + 60), int(cy)),
    (int(cx - 60), int(cy)),
    (int(cx + 30), int(cy - 30)),
    (int(cx - 30), int(cy - 30)),
]

found = False
for px, py in probes:
    print(f"center probe click @ ({px},{py})")
    cdp_click_at(px, py, clicks=1)

    deadline = time.time() + 6.0
    while time.time() < deadline and not panel_visible():
        time.sleep(0.12)

    if panel_visible():
        clicked_px = (px, py)
        out1 = "artifacts/screens/panel_after_click.png"
        driver.save_screenshot(out1)
        print("panel visible, screenshot:", out1)
        found = True
        break
    else:
        print("no panel at center probe")

# -------------------- fallback mini grid around center --------------------
if not found:
    step = 60
    half = 200
    sx = max(int(rect["left"]), int(cx - half))
    ex = min(int(rect["left"] + rect["w"]), int(cx + half))
    sy = max(int(rect["top"]),  int(cy - half))
    ey = min(int(rect["top"] + rect["h"]), int(cy + half))

    print(f"mini grid area x[{sx},{ex}] y[{sy},{ey}] step={step}")
    y = sy
    while y < ey and not found:
        x = sx
        while x < ex and not found:
            print(f"mini scan click @ ({x},{y})")
            cdp_click_at(x, y, clicks=1)

            deadline = time.time() + 6.0
            while time.time() < deadline and not panel_visible():
                time.sleep(0.12)

            if panel_visible():
                clicked_px = (x, y)
                out1 = "artifacts/screens/panel_after_click.png"
                driver.save_screenshot(out1)
                print("panel visible, screenshot:", out1)
                found = True
                break
            x += step
        y += step

if not found:
    print("No panel found near center. Check the result card/graph state.")
    time.sleep(3)
    driver.quit()
    raise SystemExit(0)

# -------------------- close panel before double-click --------------------
close_panel_if_open()

# re-read canvas rect in case layout shifted when panel was open/closed
rect2 = driver.execute_script("""
  const r = arguments[0].getBoundingClientRect();
  return {left:r.left + window.scrollX, top:r.top + window.scrollY, w:r.width, h:r.height};
""", canvas)

# keep the same internal offset inside canvas (exact same node position)
rx = clicked_px[0] - rect["left"]
ry = clicked_px[1] - rect["top"]
target_x = rect2["left"] + rx
target_y = rect2["top"]  + ry

print(f"double-click same node @ ({int(target_x)},{int(target_y)})")
cdp_click_at(target_x, target_y, clicks=2)

time.sleep(5.0)
out2 = "artifacts/screens/after_doubleclick_next_graph.png"
driver.save_screenshot(out2)
print("next graph screenshot:", out2)

time.sleep(10.0)
driver.quit()