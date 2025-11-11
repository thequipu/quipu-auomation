from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from pages.base_page import BasePage
from pages.login_page import LoginPage
import time
import os


class KnowledgeGraphPage(BasePage):
    """Page Object for Knowledge Graph Page"""

    # ========== Locators ==========
    HAMBURGER_MENU = (By.ID, 'page-menu')
    KNOWLEDGE_GRAPH_MENU = (By.ID, "Knowledge Graph-page")
    FABRIC_DROPDOWN = (By.ID, "fabric-menu")
    FABRIC_OPTION = (By.ID, "RealWorldDataMart-fabric")

    # Labels
    LABEL_LISTEDSECURITY = (By.ID, "label-listedsecurity")
    LABEL_ADDRESS = (By.ID, "label-address")

    # Node Config Panel
    NODE_CONFIG_PANEL_BTN = (By.ID, "nodeConfigPanel-btn")
    NODE_CONFIGURATION = (By.ID, "node-configuration")
    GO_BACK_BTN = (By.ID, "Go back to Node Config Panel")

    # Canvas Controls
    ZOOM_OUT_BTN = (By.ID, "graph-zoom-out-btn")
    ZOOM_IN_BTN = (By.ID, "graph-zoom-in-btn")
    FIT_TO_SCREEN_BTN = (By.ID, "graph-fit-to-screen-btn")
    CLEAR_GRAPH_BTN = (By.ID, "clearGraphView-btn")

    # Search & Query
    SEARCH_INPUT = (By.ID, "search")
    RUN_QUERY_BTN = (By.ID, "runQuery-for-result-btn")

    # Views
    TABLE_VIEW_BTN = (By.ID, "tableView-btn")
    PATH_VIEW_BTN = (By.ID, "pathView-btn")
    GRAPH_VIEW_BTN = (By.ID, "graphView-btn")

    # Canvas
    CANVAS = (By.CSS_SELECTOR, "canvas")

    # Panels
    PANEL_SELECTOR = "app-details, app-node-info, .left-container"
    BACK_BTN_CSS = "[id='Go back to Node Config Panel']"

    def __init__(self, driver):
        super().__init__(driver)
        self.actions = ActionChains(driver)

    # ========== Login ==========
    def login(self, base_url, tenant, username, password):
        """Login to the application"""
        login_page = LoginPage(self.driver)
        login_page.login(base_url, tenant, username, password)

    # ========== Navigation ==========
    def open_knowledge_graph(self):
        """Open Knowledge Graph from hamburger menu"""
        self.wait_and_click(self.HAMBURGER_MENU, sleep_after=2)
        self.wait_and_click(self.KNOWLEDGE_GRAPH_MENU, sleep_after=2)

    def select_fabric(self, fabric_name="RealWorldDataMart"):
        """Select fabric from dropdown"""
        self.wait_and_click(self.FABRIC_DROPDOWN, sleep_after=2)
        self.wait_and_click(self.FABRIC_OPTION, sleep_after=2)

    # ========== Labels ==========
    def click_label_listedsecurity(self):
        """Click on listedsecurity label"""
        self.wait_and_click(self.LABEL_LISTEDSECURITY, sleep_after=2)

    def click_label_address(self):
        """Click on address label"""
        self.wait_and_click(self.LABEL_ADDRESS, sleep_after=3)

    # ========== Node Config Panel ==========
    def open_node_config_panel(self):
        """Open node configuration panel"""
        self.wait_and_click(self.NODE_CONFIG_PANEL_BTN, sleep_after=1)

    def open_node_configuration(self):
        """Open node configuration"""
        self.wait_and_click(self.NODE_CONFIGURATION, sleep_after=1)

    def back_from_node_config_panel(self):
        """Go back from node config panel"""
        self.wait_and_click(self.GO_BACK_BTN, sleep_after=1)

    # ========== Canvas Controls ==========
    def zoom_out(self):
        """Zoom out the graph"""
        self.wait_and_click(self.ZOOM_OUT_BTN, sleep_after=1)

    def zoom_in(self, times=1):
        """Zoom in the graph"""
        for _ in range(times):
            self.wait_and_click(self.ZOOM_IN_BTN, sleep_after=1)

    def fit_to_screen(self):
        """Fit graph to screen"""
        self.wait_and_click(self.FIT_TO_SCREEN_BTN, sleep_after=5)

    def clear_graph_view(self):
        """Clear the graph view"""
        self.wait_and_click(self.CLEAR_GRAPH_BTN, sleep_after=5)

    # ========== Search & Query ==========
    def search_and_enter(self, search_text):
        """Search for text and press enter"""
        search_box = self.find_element(self.SEARCH_INPUT)
        search_box.send_keys(search_text)
        search_box.send_keys(Keys.ENTER)
        time.sleep(2)

    def run_query(self):
        """Click run query button"""
        self.wait_and_click(self.RUN_QUERY_BTN, sleep_after=5)

    # ========== View Controls ==========
    def click_table_view(self):
        """Switch to table view"""
        self.wait_and_click(self.TABLE_VIEW_BTN, sleep_after=1)

    def click_path_view(self):
        """Switch to path view"""
        self.wait_and_click(self.PATH_VIEW_BTN, sleep_after=1)

    def click_graph_view(self):
        """Switch to graph view"""
        self.wait_and_click(self.GRAPH_VIEW_BTN, sleep_after=1)

    # ========== Canvas Helpers ==========
    def get_canvas(self):
        """Get canvas element and scroll into view"""
        canvas = self.wait.until(EC.visibility_of_element_located(self.CANVAS))
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center', inline:'center'});", canvas)
        time.sleep(0.3)
        return canvas

    def get_canvas_rect(self, canvas):
        """Get canvas position and size"""
        rect = self.driver.execute_script("""
          const r = arguments[0].getBoundingClientRect();
          return {left:r.left + window.scrollX, top:r.top + window.scrollY, w:r.width, h:r.height};
        """, canvas)
        return rect

    def get_canvas_rect_viewport(self, canvas):
        """Get canvas position (viewport coords)"""
        rect = self.driver.execute_script("""
          const r = arguments[0].getBoundingClientRect();
          return {left:r.left, top:r.top, w:r.width, h:r.height};
        """, canvas)
        return rect

    # ========== Panel Helpers ==========
    def panel_visible(self):
        """Check if node details panel is visible"""
        try:
            els = self.driver.find_elements(By.CSS_SELECTOR, self.PANEL_SELECTOR)
            return any(e.is_displayed() for e in els)
        except:
            return False

    def click_back_panel(self):
        """Click back button to close panel"""
        try:
            btn = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, self.BACK_BTN_CSS)))
            btn.click()
            self.wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, self.PANEL_SELECTOR)))
            print("back clicked, panel closed")
        except:
            print("back not clickable/visible")

    # ========== CDP Click Methods ==========
    def cdp_click_at(self, cx, cy, clicks=1):
        """Click at coordinates using CDP - clicks=2 for double-click"""
        self.driver.execute_cdp_cmd("Input.dispatchMouseEvent",
                                    {"type": "mouseMoved", "x": float(cx), "y": float(cy), "buttons": 1})
        self.driver.execute_cdp_cmd("Input.dispatchMouseEvent",
                                    {"type": "mousePressed", "x": float(cx), "y": float(cy),
                                     "button": "left", "buttons": 1, "clickCount": clicks})
        self.driver.execute_cdp_cmd("Input.dispatchMouseEvent",
                                    {"type": "mouseReleased", "x": float(cx), "y": float(cy),
                                     "button": "left", "buttons": 1, "clickCount": clicks})

    # ========== Node Click Methods ==========
    def scan_and_click_node(self, step=80):
        """Scan canvas and click first node found"""
        os.makedirs("artifacts/screens", exist_ok=True)

        canvas = self.get_canvas()
        rect = self.get_canvas_rect(canvas)

        clicked_px = None
        sx, ex = int(rect["left"] + 200), int(rect["left"] + rect["w"] - 20)
        sy, ey = int(rect["top"] + 40), int(rect["top"] + rect["h"] - 40)

        found = False
        y = sy
        while y < ey and not found:
            x = sx
            while x < ex and not found:
                print(f"scan click @ ({x},{y})")
                self.cdp_click_at(x, y, clicks=1)

                end = time.time() + 6
                while time.time() < end and not self.panel_visible():
                    time.sleep(0.1)

                if self.panel_visible():
                    clicked_px = (x, y)
                    out1 = "artifacts/screens/panel_after_click.png"
                    self.driver.save_screenshot(out1)
                    print("panel screenshot:", out1)
                    found = True
                    break
                x += step
            y += step

        if not found:
            print("No panel found.")
            return None

        return clicked_px

    def double_click_node_at(self, x, y):
        """Double-click at specific coordinates"""
        print(f"double-click node @ ({x},{y})")
        self.cdp_click_at(x, y, clicks=2)
        time.sleep(5)
        out2 = "artifacts/screens/after_doubleclick_next_graph.png"
        self.driver.save_screenshot(out2)
        print("next graph screenshot:", out2)

    # ========== Node Dots (Click 2 nodes) ==========
    def get_node_info_from_graph(self):
        """Try to get first 2 nodes from graph libraries"""
        node_info = self.driver.execute_script("""
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
        return node_info

    def fire_graph_events(self, lib, node_id):
        """Fire library events for node"""
        try:
            self.driver.execute_script("""
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

    def click_two_nodes_with_screenshots(self, step=80):
        """Click first 2 nodes and take screenshots"""
        os.makedirs("artifacts/screens", exist_ok=True)

        canvas = self.get_canvas()
        rect = self.get_canvas_rect_viewport(canvas)

        node_info = self.get_node_info_from_graph()
        shots = 0

        # Try deterministic clicks first
        for n in node_info[:2]:
            if shots >= 2:
                break

            self.fire_graph_events(n["lib"], n["id"])

            vx = rect["left"] + max(1, min(rect["w"] - 2, int(n["x"])))
            vy = rect["top"] + max(1, min(rect["h"] - 2, int(n["y"])))
            print(f"node click {n['id']} @ ({vx:.1f},{vy:.1f}) lib={n['lib']}")
            self.cdp_click_at(vx, vy)

            end = time.time() + 3.5
            while time.time() < end and not self.panel_visible():
                time.sleep(0.1)

            time.sleep(0.7)
            self.driver.save_screenshot(f"artifacts/screens/dot_{shots + 1}.png")
            print(("panel visible," if self.panel_visible() else "no panel,"),
                  f"screenshot: artifacts/screens/dot_{shots + 1}.png")

            if self.panel_visible():
                shots += 1
                self.click_back_panel()
                time.sleep(0.4)

        # Fallback: grid scan
        if shots < 2:
            left_margin, top_margin, right_margin, bottom_margin = 200, 40, 20, 40
            sx = max(1, left_margin)
            ex = int(rect["w"] - right_margin)
            sy = max(1, top_margin)
            ey = int(rect["h"] - bottom_margin)

            y = sy
            while y < ey and shots < 2:
                x = sx
                while x < ex and shots < 2:
                    vx = rect["left"] + x
                    vy = rect["top"] + y
                    print(f"scan click @ ({vx:.1f},{vy:.1f}) from ({x},{y})")
                    self.cdp_click_at(vx, vy)

                    end = time.time() + 3.0
                    while time.time() < end and not self.panel_visible():
                        time.sleep(0.1)

                    time.sleep(0.5)
                    self.driver.save_screenshot(f"artifacts/screens/dot_{shots + 1}.png")
                    print(("panel visible," if self.panel_visible() else "no panel,"),
                          f"screenshot: artifacts/screens/dot_{shots + 1}.png")

                    if self.panel_visible():
                        shots += 1
                        self.click_back_panel()
                        time.sleep(0.3)

                    x += step
                y += step

        print(f"total panel screenshots captured: {shots}")
        return shots

    # ========== Tooltip Collection ==========
    def is_element_visible(self, element):
        """Check if element is truly visible"""
        try:
            if not element.is_displayed():
                return False
            rect = element.rect
            return rect.get("width", 0) > 0 and rect.get("height", 0) > 0
        except:
            return False

    def get_relationship_chips(self):
        """Find relationship chips in the Relationships section"""
        section = None
        for cand in self.driver.find_elements(By.XPATH, "//div[.//text()[contains(., 'Relationships')]]"):
            if cand.is_displayed():
                section = cand
                break
        if not section:
            return []

        candidates = []
        xps = [
            ".//button[normalize-space()!='']",
            ".//*[contains(@class,'chip')]",
            ".//*[contains(@class,'tag')]",
            ".//span[normalize-space()!='' and not(*)]",
            ".//a[normalize-space()!='']"
        ]
        for xp in xps:
            candidates.extend(section.find_elements(By.XPATH, xp))

        return [el for el in candidates if self.is_element_visible(el)]

    def get_tooltip_text(self, target):
        """Get tooltip text from element"""
        # Try aria-describedby
        try:
            tid = target.get_attribute("aria-describedby")
            if tid:
                t = self.driver.execute_script(
                    "var n=document.getElementById(arguments[0]); return n? n.innerText.trim():'';", tid)
                if t:
                    return t
        except:
            pass

        # Try overlay containers
        overlay_selectors = [
            ".cdk-overlay-container .mat-tooltip",
            ".cdk-overlay-container [role='tooltip']",
            ".cdk-overlay-container .mat-tooltip-panel",
            "[role='tooltip']",
            ".tooltip",
            ".ngx-tooltip",
            "[class*='tooltip']"
        ]
        end = time.time() + 2.5
        while time.time() < end:
            for sel in overlay_selectors:
                els = self.driver.find_elements(By.CSS_SELECTOR, sel)
                for el in els:
                    try:
                        if self.is_element_visible(el):
                            txt = el.text.strip()
                            if txt:
                                return txt
                    except:
                        continue
            time.sleep(0.1)

        # Try element attributes
        for attr in ["title", "aria-label", "data-tooltip", "data-title"]:
            val = (target.get_attribute(attr) or "").strip()
            if val:
                return val

        return ""

    def collect_relationship_tooltips(self):
        """Collect all relationship tooltips and return as list"""
        print("Collecting relationship tooltips")
        chips = self.get_relationship_chips()
        print(f"Found {len(chips)} visible relationship chips")

        rows = []
        for idx, chip in enumerate(chips, 1):
            try:
                self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", chip)
                time.sleep(0.3)
                self.actions.move_to_element(chip).perform()
                time.sleep(1.2)
                tip = self.get_tooltip_text(chip)
                name = chip.text.strip() or f"Relationship_{idx}"
                if not tip:
                    tip = "no tooltip"
                rows.append({"Relationship": name, "Tooltip": tip})
                print(f"{idx}. {name} -> {tip}")
            except Exception as e:
                print(f"{idx}. hover/read failed: {e}")

        return rows

    def collect_simple_tooltips(self):
        """Simple tooltip collection from relationship elements"""
        print("Collecting relationship tooltips...")
        tooltip_data = []

        relationship_elements = self.driver.find_elements(By.CSS_SELECTOR, ".relationship, .ng-star-inserted")

        for rel in relationship_elements:
            try:
                self.driver.execute_script("arguments[0].scrollIntoView(true);", rel)
                time.sleep(1)
                self.actions.move_to_element(rel).perform()
                time.sleep(2)
                tooltip = rel.get_attribute("title") or rel.text
                text_value = rel.text.strip() if rel.text.strip() else "Unnamed"
                tooltip_text = tooltip.strip() if tooltip else "No tooltip found"
                tooltip_data.append({"Relationship": text_value, "Tooltip": tooltip_text})
                print(f"{text_value} - {tooltip_text}")
            except Exception as e:
                print(f"Error while reading tooltip: {str(e)}")

        return tooltip_data