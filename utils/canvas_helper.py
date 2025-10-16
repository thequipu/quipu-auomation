# utils/canvas_helper.py
import os, time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

PANEL_SELECTOR = "app-details"
BACK_BTN       = "[id='Go back to Node Config Panel']"  # id contains spaces

def ensure_artifacts_dir():
    os.makedirs("artifacts/screens", exist_ok=True)

def panel_visible(driver):
    try:
        el = driver.find_element(By.CSS_SELECTOR, PANEL_SELECTOR)
        return el.is_displayed()
    except:
        return False

def click_back(driver, timeout=10):
    try:
        btn = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.CSS_SELECTOR, BACK_BTN)))
        btn.click()
        WebDriverWait(driver, timeout).until(EC.invisibility_of_element_located((By.CSS_SELECTOR, PANEL_SELECTOR)))
        print("back clicked, panel closed")
    except:
        print("back not clickable/visible")

def cdp_click_at(driver, cx, cy):
    # Chrome DevTools Protocol click at absolute viewport coords
    driver.execute_cdp_cmd("Input.dispatchMouseEvent", {"type": "mouseMoved",   "x": float(cx), "y": float(cy), "buttons": 1})
    driver.execute_cdp_cmd("Input.dispatchMouseEvent", {"type": "mousePressed", "x": float(cx), "y": float(cy), "button": "left", "buttons": 1, "clickCount": 1})
    driver.execute_cdp_cmd("Input.dispatchMouseEvent", {"type": "mouseReleased","x": float(cx), "y": float(cy), "button": "left", "buttons": 1, "clickCount": 1})

def get_canvas(driver, wait_timeout=20):
    wait = WebDriverWait(driver, wait_timeout)
    canvas = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "canvas")))
    driver.execute_script("arguments[0].scrollIntoView({block:'center', inline:'center'});", canvas)
    time.sleep(0.3)
    return canvas

def get_canvas_rect(driver, canvas):
    return driver.execute_script("""
      const r = arguments[0].getBoundingClientRect();
      return {left:r.left, top:r.top, w:r.width, h:r.height};
    """, canvas)

def get_node_info_via_js(driver):
    # Try to extract first 2 node positions from common graph libs (cytoscape/vis.js)
    return driver.execute_script("""
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

def fire_library_node_events(driver, lib, node_id):
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
        """, lib, node_id)
    except:
        pass

def bounded_click(driver, rect, x, y):
    vx = rect["left"] + max(1, min(rect["w"]-2, int(x)))
    vy = rect["top"]  + max(1, min(rect["h"]-2, int(y)))
    cdp_click_at(driver, vx, vy)
    return vx, vy

def capture_panel_screenshots(driver, rect, want=2, prefix="dot_"):
    ensure_artifacts_dir()
    shots = 0

    # first: deterministic clicks using JS node info
    node_info = get_node_info_via_js(driver)
    for n in node_info[:2]:
        if shots >= want: break
        fire_library_node_events(driver, n["lib"], n["id"])
        vx, vy = bounded_click(driver, rect, n["x"], n["y"])
        print(f"node click {n['id']} @ ({vx:.1f},{vy:.1f}) lib={n['lib']}")
        end = time.time() + 3.5
        while time.time() < end and not panel_visible(driver):
            time.sleep(0.1)
        time.sleep(0.7)
        path = f"artifacts/screens/{prefix}{shots+1}.png"
        driver.save_screenshot(path)
        print(("panel visible," if panel_visible(driver) else "no panel,"), f"screenshot: {path}")
        if panel_visible(driver):
            shots += 1
            click_back(driver)
            time.sleep(0.4)

    # fallback: scan grid until we have enough
    if shots < want:
        step = 80
        left_margin, top_margin, right_margin, bottom_margin = 200, 40, 20, 40
        sx = max(1, left_margin); ex = int(rect["w"] - right_margin)
        sy = max(1, top_margin);  ey = int(rect["h"] - bottom_margin)
        y = sy
        while y < ey and shots < want:
            x = sx
            while x < ex and shots < want:
                vx = rect["left"] + x
                vy = rect["top"]  + y
                print(f"scan click @ ({vx:.1f},{vy:.1f}) from ({x},{y})")
                cdp_click_at(driver, vx, vy)
                end = time.time() + 3.0
                while time.time() < end and not panel_visible(driver):
                    time.sleep(0.1)
                time.sleep(0.5)
                path = f"artifacts/screens/{prefix}{shots+1}.png"
                driver.save_screenshot(path)
                print(("panel visible," if panel_visible(driver) else "no panel,"), f"screenshot: {path}")
                if panel_visible(driver):
                    shots += 1
                    click_back(driver)
                    time.sleep(0.3)
                x += step
            y += step

    print(f"total panel screenshots captured: {shots}")
    return shots