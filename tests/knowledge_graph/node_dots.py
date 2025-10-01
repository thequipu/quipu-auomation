import os, time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# -------------------- setup + login --------------------
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 20)

driver.get("http://localhost:4200/login")
driver.maximize_window()

tenant_input = wait.until(EC.presence_of_element_located((By.ID, "tenantId")))
tenant_input.send_keys("preprodquipuai1")
time.sleep(1)

proceed_btn = wait.until(EC.element_to_be_clickable((By.ID, "tenant-btn")))
proceed_btn.click()

username_input = wait.until(EC.presence_of_element_located((By.ID, "username")))
username_input.send_keys("narenm")

password_input = wait.until(EC.presence_of_element_located((By.ID, "password")))
password_input.send_keys("12!Quipu345")

login_btn = wait.until(EC.element_to_be_clickable((By.ID, "signIn-btn")))
login_btn.click()

# -------------------- navigate to KG --------------------
hamburger_icon = wait.until(EC.element_to_be_clickable((By.ID, "page-menu")))
hamburger_icon.click(); time.sleep(2)

knowledgegraps = wait.until(EC.element_to_be_clickable((By.ID, "Knowledge Graph-page")))
knowledgegraps.click(); time.sleep(2)

fabricpage_dropdown = wait.until(EC.presence_of_element_located((By.ID, "fabric-menu")))
fabricpage_dropdown.click(); time.sleep(2)

dropdown = wait.until(EC.presence_of_element_located((By.ID, "RealWorldDataMart-fabric")))
dropdown.click(); time.sleep(2)

#search_input = wait.until(EC.presence_of_element_located((By.ID, "search")))
#search_input.send_keys("address"); search_input.send_keys(Keys.ENTER); time.sleep(1.5)

#run_icon_btn = wait.until(EC.element_to_be_clickable((By.ID, "runQuery-for-result-btn")))
#run_icon_btn.click()
address_btn = wait.until(EC.element_to_be_clickable((By.ID,"label-address")))
address_btn.click()
time.sleep(3)

# -------------------- helpers --------------------
PANEL_SELECTOR = "app-details"
BACK_BTN       = "[id='Go back to Node Config Panel']"  # id contains spaces

def panel_visible():
    try:
        el = driver.find_element(By.CSS_SELECTOR, PANEL_SELECTOR)
        return el.is_displayed()
    except:
        return False

def click_back():
    try:
        btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, BACK_BTN)))
        btn.click()
        WebDriverWait(driver, 10).until(EC.invisibility_of_element_located((By.CSS_SELECTOR, PANEL_SELECTOR)))
        print("back clicked, panel closed")
    except:
        print("back not clickable/visible")

def cdp_click_at(cx, cy):
    # real mouse events via Chrome DevTools Protocol
    driver.execute_cdp_cmd("Input.dispatchMouseEvent", {"type": "mouseMoved",   "x": float(cx), "y": float(cy), "buttons": 1})
    driver.execute_cdp_cmd("Input.dispatchMouseEvent", {"type": "mousePressed", "x": float(cx), "y": float(cy), "button": "left", "buttons": 1, "clickCount": 1})
    driver.execute_cdp_cmd("Input.dispatchMouseEvent", {"type": "mouseReleased","x": float(cx), "y": float(cy), "button": "left", "buttons": 1, "clickCount": 1})

# -------------------- canvas --------------------
canvas = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "canvas")))
driver.execute_script("arguments[0].scrollIntoView({block:'center', inline:'center'});", canvas)
time.sleep(0.3)

os.makedirs("artifacts/screens", exist_ok=True)

# canvas rect (viewport coords)
rect = driver.execute_script("""
  const r = arguments[0].getBoundingClientRect();
  return {left:r.left, top:r.top, w:r.width, h:r.height};
""", canvas)

# try to get first 2 nodes from graph libs (Cytoscape/vis.js)
node_info = driver.execute_script("""
  try {
    if (window.cy && typeof cy.nodes==='function') {
      return cy.nodes().slice(0,2).map(n => {
        const p = n.renderedPosition(); return {lib:'cy', id:n.id(), x:p.x, y:p.y};
      });
    }
    if (window.network && network.getPositions) {
      const ids = Object.keys(network.getPositions()).slice(0,2);
      const scale = network.getScale(), view = network.getViewPosition();
      const cx = network.canvas.body.view.area.center.x, cy = network.canvas.body.view.area.center.y;
      return ids.map(id => {
        const p = network.getPositions([id])[id];
        return {lib:'vis', id, x:(p.x-view.x)*scale+cx, y:(p.y-view.y)*scale+cy};
      });
    }
  } catch(e) {}
  return [];
""") or []

shots = 0

# ---------- deterministic: click first two nodes if available ----------
for n in node_info[:2]:
    if shots >= 2: break

    # fire library events (best-effort)
    try:
        driver.execute_script("""
          try {
            if (arguments[0]==='cy' && window.cy) {
              const el = cy.getElementById(arguments[1]);
              if (el && el.length) { try{ cy.center(el); }catch(e){} el.emit('tap'); el.emit('click'); }
            }
            if (arguments[0]==='vis' && window.network) {
              const id = arguments[1];
              try{ network.focus(id, {animation:true}); }catch(e){}
              try{ network.selectNodes([id], false); }catch(e){}
              try{ network.emit('selectNode', {nodes:[id]}); }catch(e){}
              try{ network.emit('click', {nodes:[id], edges:[], event:{isTrusted:true}}); }catch(e){}
            }
          } catch(e) {}
        """, n["lib"], n["id"])
    except:
        pass

    vx = rect["left"] + max(1, min(rect["w"]-2, int(n["x"])))
    vy = rect["top"]  + max(1, min(rect["h"]-2, int(n["y"])))
    print(f"node click {n['id']} @ ({vx:.1f},{vy:.1f}) lib={n['lib']}")
    cdp_click_at(vx, vy)

    end = time.time() + 3.5
    while time.time() < end and not panel_visible():
        time.sleep(0.1)

    time.sleep(0.7)
    driver.save_screenshot(f"artifacts/screens/dot_{shots+1}.png")
    print(("panel visible," if panel_visible() else "no panel,"), f"screenshot: artifacts/screens/dot_{shots+1}.png")

    if panel_visible():
        shots += 1
        click_back()
        time.sleep(0.4)

# ---------- fallback: small grid until 2 panels ----------
if shots < 2:
    step = 80
    left_margin, top_margin, right_margin, bottom_margin = 200, 40, 20, 40
    sx = max(1, left_margin); ex = int(rect["w"] - right_margin)
    sy = max(1, top_margin);  ey = int(rect["h"] - bottom_margin)

    y = sy
    while y < ey and shots < 2:
        x = sx
        while x < ex and shots < 2:
            vx = rect["left"] + x
            vy = rect["top"]  + y
            print(f"scan click @ ({vx:.1f},{vy:.1f}) from ({x},{y})")
            cdp_click_at(vx, vy)

            end = time.time() + 3.0
            while time.time() < end and not panel_visible():
                time.sleep(0.1)

            time.sleep(0.5)
            driver.save_screenshot(f"artifacts/screens/dot_{shots+1}.png")
            print(("panel visible," if panel_visible() else "no panel,"), f"screenshot: artifacts/screens/dot_{shots+1}.png")

            if panel_visible():
                shots += 1
                click_back()
                time.sleep(0.3)

            x += step
        y += step

print(f"total panel screenshots captured: {shots}")
time.sleep(1.0)
driver.quit()