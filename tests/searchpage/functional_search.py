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
search_text = "liam Gurret"   # reuse this to find the node by label
search_input.send_keys(search_text)
search_input.send_keys(Keys.ENTER)
time.sleep(5)

# -------------------- helpers --------------------
PANEL_SELECTOR = "app-details, app-node-info, .left-container"

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

def canvas_rect(elem):
    return driver.execute_script("""
      const r = arguments[0].getBoundingClientRect();
      return {left:r.left + window.scrollX, top:r.top + window.scrollY, w:r.width, h:r.height};
    """, elem)

def canvas_hash(prefix_len=120):
    return driver.execute_script("""
      const c = document.querySelector('canvas');
      if (!c) return null;
      try { return c.toDataURL('image/png').slice(0, arguments[0]); } catch(e) { return null; }
    """, prefix_len)

# find node by visible label (Cytoscape or vis.js)
def find_node_position_by_name(name):
    js = """
    const want = arguments[0];
    // Cytoscape
    try {
      if (window.cy && typeof cy.nodes==='function') {
        let els = cy.nodes().filter(n => {
          const nm = (n.data('name') ?? n.data('label') ?? n.id() ?? '').toString();
          return nm.trim().toLowerCase() === want.trim().toLowerCase();
        });
        if (els && els.length > 0) {
          const n  = els[0];
          const rp = n.renderedPosition();
          return {lib:'cy', id:n.id(), x: rp.x, y: rp.y};
        }
      }
    } catch(e) {}
    // vis.js
    try {
      if (window.network && network.body && network.getPositions) {
        const nodes = network.body.data.nodes.get();
        const cand = nodes.find(n => {
          const nm = (n.label ?? n.id ?? '').toString();
          return nm.trim().toLowerCase() === want.trim().toLowerCase();
        });
        if (cand) {
          const pos = network.getPositions([cand.id])[cand.id];
          const scale = network.getScale();
          const view  = network.getViewPosition();
          const cx = network.canvas.body.view.area.center.x;
          const cy = network.canvas.body.view.area.center.y;
          const rx = (pos.x - view.x) * scale + cx;
          const ry = (pos.y - view.y) * scale + cy;
          return {lib:'vis', id: cand.id, x: rx, y: ry};
        }
      }
    } catch(e) {}
    return null;
    """
    try:
        return driver.execute_script(js, name)
    except:
        return None

# -------------------- canvas --------------------
canvas = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "canvas")))
driver.execute_script("arguments[0].scrollIntoView({block:'center', inline:'center'});", canvas)
time.sleep(0.4)

rect = canvas_rect(canvas)

# 1) try find-by-name
clicked_px = None
info = find_node_position_by_name(search_text)
if info:
    x = rect["left"] + max(1, min(rect["w"]-2, int(info["x"])))
    y = rect["top"]  + max(1, min(rect["h"]-2, int(info["y"])))
    print(f"click '{search_text}' @ ({x:.1f},{y:.1f}) lib={info['lib']} id={info['id']}")
    cdp_click_at(x, y, clicks=1)
    clicked_px = (x, y)

    # wait for panel
    end = time.time() + 8
    while time.time() < end and not panel_visible():
        time.sleep(0.12)

# 2) fallback: small center probes if panel not visible
if not panel_visible():
    cx = int(rect["left"] + rect["w"]/2); cy = int(rect["top"] + rect["h"]/2)
    for dx,dy in [(0,0),(30,0),(-30,0),(0,30),(0,-30),(60,0),(-60,0),(30,-30),(-30,-30)]:
        px, py = cx+dx, cy+dy
        print(f"center probe click @ ({px},{py})")
        cdp_click_at(px, py, clicks=1)
        end = time.time() + 6
        while time.time() < end and not panel_visible():
            time.sleep(0.12)
        if panel_visible():
            clicked_px = (px, py)
            break

if not panel_visible():
    print("Panel did not appear. Adjust name match or probes.")
    time.sleep(5)
    driver.quit()
    raise SystemExit(0)

print("panel opened")

# -------------------- click the Open button in panel, wait for graph change, screenshot --------------------
# record canvas fingerprint BEFORE clicking the open button
before_hash = canvas_hash()

open_btn_xpath = '//*[@id="ngb-accordion-item-100-collapse"]/div/app-search-result/div/app-graph-viz/div/as-split/as-split-area[2]/div/div/div/div[2]/div[2]/app-details/div/app-node-info/div/div[1]/div[1]/div[2]/button[1]'
open_btn = wait.until(EC.element_to_be_clickable((By.XPATH, open_btn_xpath)))
open_btn.click()
print("Open button clicked.")

# wait for canvas redraw/change (hash-based, up to ~10s)
changed = False
end = time.time() + 10
while time.time() < end:
    time.sleep(0.5)
    after_hash = canvas_hash()
    if after_hash and before_hash and after_hash != before_hash:
        changed = True
        break

os.makedirs("artifacts/screens", exist_ok=True)
out = "artifacts/screens/after_open_button.png"
driver.save_screenshot(out)
print(("graph changed, " if changed else "graph unchanged (timed), ") + f"screenshot: {out}")

# keep page open for inspection / further steps
time.sleep(10)
driver.quit()