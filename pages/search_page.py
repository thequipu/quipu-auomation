# pages/search_page.py
import os
import time
from typing import Optional, Tuple

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SearchPage:
    """
    POM for the Search page.
    IMPORTANT: Keeps your exact IDs and sleeps. We only add robust fallbacks,
    no changes to your given IDs/XPaths.
    """

    # --- IDs you already use ---
    FABRIC_MENU = (By.ID, "fabric-menu")
    HETIONET_FABRIC = (By.ID, "Hetionet-fabric")
    REALWORLDDATAMART_FABRIC = (By.ID, "RealWorldDataMart-fabric")
    SEARCH_INPUT = (By.ID, "search-query")
    TABLEVIEW_BTN = (By.ID, "tableView-btn")

    # Node details panel selectors you already used
    PANEL_SELECTOR = (By.CSS_SELECTOR, "app-details, app-node-info, .left-container")

    def __init__(self, driver, wait: WebDriverWait):
        self.driver = driver
        self.wait = wait

    # ----------------------- Fabric open helpers (EXACT IDs + time.sleep) -----------------------
    def open_hetionet_fabric(self):
        self.wait.until(EC.presence_of_element_located(self.FABRIC_MENU)).click()
        time.sleep(2)
        self.wait.until(EC.presence_of_element_located(self.HETIONET_FABRIC)).click()
        time.sleep(2)

    def open_realworlddatamart_fabric(self):
        self.wait.until(EC.presence_of_element_located(self.FABRIC_MENU)).click()
        time.sleep(2)
        self.wait.until(EC.presence_of_element_located(self.REALWORLDDATAMART_FABRIC)).click()
        time.sleep(2)

    def open_fabric_menu(self, name: str):
        """Generic open by fabric name if you want it."""
        self.wait.until(EC.presence_of_element_located(self.FABRIC_MENU)).click()
        time.sleep(2)
        if name.strip().lower().startswith("het"):
            self.wait.until(EC.presence_of_element_located(self.HETIONET_FABRIC)).click()
        else:
            self.wait.until(EC.presence_of_element_located(self.REALWORLDDATAMART_FABRIC)).click()
        time.sleep(2)

    # ----------------------- Search box (EXACT ID) -----------------------
    def type_search_and_submit(self, text: str):
        box = self.wait.until(EC.presence_of_element_located(self.SEARCH_INPUT))
        try:
            box.clear()
        except Exception:
            pass
        box.send_keys(text)
        box.submit()
        # Your UI is slow; keep the pause.
        time.sleep(5)

    # ----------------------- Panel visibility (your CSS) -----------------------
    def panel_visible(self) -> bool:
        try:
            els = self.driver.find_elements(*self.PANEL_SELECTOR)
            return any(e.is_displayed() for e in els)
        except Exception:
            return False

    # ----------------------- Canvas helpers (for node clicks + hash) -----------------------
    def _canvas(self):
        return self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "canvas")))

    def canvas_rect(self, elem) -> dict:
        return self.driver.execute_script("""
          const r = arguments[0].getBoundingClientRect();
          return {left:r.left + window.scrollX, top:r.top + window.scrollY, w:r.width, h:r.height};
        """, elem)

    def canvas_hash(self, prefix_len=120) -> Optional[str]:
        try:
            return self.driver.execute_script("""
              const c = document.querySelector('canvas');
              if (!c) return null;
              try { return c.toDataURL('image/png').slice(0, arguments[0]); } catch(e) { return null; }
            """, prefix_len)
        except Exception:
            return None

    def cdp_click_at(self, cx, cy, clicks=1):
        self.driver.execute_cdp_cmd("Input.dispatchMouseEvent",
            {"type": "mouseMoved", "x": float(cx), "y": float(cy), "buttons": 1})
        self.driver.execute_cdp_cmd("Input.dispatchMouseEvent",
            {"type": "mousePressed", "x": float(cx), "y": float(cy),
             "button": "left", "buttons": 1, "clickCount": clicks})
        self.driver.execute_cdp_cmd("Input.dispatchMouseEvent",
            {"type": "mouseReleased", "x": float(cx), "y": float(cy),
             "button": "left", "buttons": 1, "clickCount": clicks})

    # ----------------------- Try click node by visible label first, else probe center -----------------------
    def click_node_by_name_or_probe(self, name: str, wait_panel_seconds: float = 8.0, allow_wide_scan: bool = True) -> Optional[Tuple[int, int]]:
        canvas = self._canvas()
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center', inline:'center'});", canvas)
        time.sleep(0.6)
        rect = self.canvas_rect(canvas)

        # 1) Try to compute node position by name from common libs (Cytoscape/vis.js)
        info = self._find_node_position_by_name(name)
        clicked_px = None
        if info:
            x = rect["left"] + max(1, min(rect["w"] - 2, int(info["x"])))
            y = rect["top"] + max(1, min(rect["h"] - 2, int(info["y"])))
            self.cdp_click_at(x, y, clicks=1)
            clicked_px = (x, y)
            end = time.time() + wait_panel_seconds
            while time.time() < end and not self.panel_visible():
                time.sleep(0.15)

        # 2) Fallback: small center probes
        if not self.panel_visible():
            cx = int(rect["left"] + rect["w"] / 2)
            cy = int(rect["top"] + rect["h"] / 2)
            for dx, dy in [(0, 0), (30, 0), (-30, 0), (0, 30), (0, -30), (60, 0), (-60, 0), (30, -30), (-30, -30)]:
                px, py = cx + dx, cy + dy
                self.cdp_click_at(px, py, clicks=1)
                end = time.time() + 6
                while time.time() < end and not self.panel_visible():
                    time.sleep(0.12)
                if self.panel_visible():
                    clicked_px = (px, py)
                    break

        # 3) Last resort: wide scan across the canvas (keeps your UI slow behavior in mind)
        if not self.panel_visible() and allow_wide_scan:
            clicked_px = self._wide_scan_for_panel(rect, total_seconds=22, step=90)

        return clicked_px

    def _find_node_position_by_name(self, name: str):
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
            return self.driver.execute_script(js, name)
        except Exception:
            return None

    # ----------------------- Table view (EXACT ID) -----------------------
    def click_table_view(self):
        tableview_btn = self.wait.until(EC.presence_of_element_located(self.TABLEVIEW_BTN))
        tableview_btn.click()
        time.sleep(2)

    # ----------------------- Your exact Open-button XPath, but more robust -----------------------
    def click_open_button_xpath(self, xpath: str, wait_for_graph_change_seconds: float = 10.0) -> bool:
        """
        Uses your exact XPath. No locator changes.
        Adds: presence wait, scrollIntoView, ActionChains move, JS click fallback, and a small retry.
        Also compares canvas hash before/after (non-fatal).
        """
        # Canvas hash before (if present)
        before_hash = self.canvas_hash()

        # 1) Wait for presence first (less strict than clickable)
        btn = self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))

        # 2) Scroll into view
        try:
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center', inline:'center'});", btn)
            time.sleep(0.4)
        except Exception:
            pass

        # 3) Move to element (helps hover/visibility)
        try:
            ActionChains(self.driver).move_to_element(btn).pause(0.2).perform()
        except Exception:
            pass

        # 4) Try normal clickable click
        try:
            btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            btn.click()
        except Exception:
            # 5) Fallback: JS click with the SAME xpath element
            try:
                self.driver.execute_script("arguments[0].click();", btn)
            except Exception:
                # 6) Small retry: re-find + JS click
                try:
                    btn2 = self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
                    self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn2)
                    time.sleep(0.3)
                    self.driver.execute_script("arguments[0].click();", btn2)
                except Exception:
                    os.makedirs("artifacts/screens", exist_ok=True)
                    self.driver.save_screenshot("artifacts/screens/failed_click_open_button.png")
                    raise

        # 7) Optionally wait for canvas change
        changed = False
        end = time.time() + max(1.0, wait_for_graph_change_seconds)
        while time.time() < end:
            time.sleep(0.5)
            after_hash = self.canvas_hash()
            if after_hash and before_hash and after_hash != before_hash:
                changed = True
                break

        return changed

    # ----------------------- Wide scan across the canvas (no locator changes) -----------------------
    def _wide_scan_for_panel(self, rect: dict, total_seconds: int = 22, step: int = 90) -> Optional[Tuple[int, int]]:
        """
        As a last resort, slowly scan across the canvas and click points on a grid
        until panel becomes visible. Keeps your slow UI in mind.
        """
        start = time.time()
        clicked_px = None

        left = int(rect["left"])
        top = int(rect["top"])
        right = int(rect["left"] + rect["w"])
        bottom = int(rect["top"] + rect["h"])

        y = top + 30
        while y < bottom - 30 and (time.time() - start) < total_seconds and not self.panel_visible():
            x = left + 30
            while x < right - 30 and (time.time() - start) < total_seconds and not self.panel_visible():
                self.cdp_click_at(x, y, clicks=1)
                end = time.time() + 1.5
                while time.time() < end and not self.panel_visible():
                    time.sleep(0.12)
                if self.panel_visible():
                    clicked_px = (x, y)
                    break
                x += step
            y += step

        return clicked_px