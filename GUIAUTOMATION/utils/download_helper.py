import os, time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import pyautogui

# --- download helpers ---
def wait_for_download(dir_path: str, timeout: int = 120):
    end = time.time() + timeout
    while time.time() < end:
        try:
            done = []
            for f in os.listdir(dir_path):
                if f.startswith('.'):
                    continue
                if f.endswith('.crdownload') or f.endswith('.tmp'):
                    continue
                full = os.path.join(dir_path, f)
                if os.path.isfile(full):
                    done.append(full)
            if done:
                # return the most recent completed file
                return max(done, key=os.path.getmtime)
        except FileNotFoundError:
            pass
        time.sleep(1)
    raise TimeoutError("Download did not complete in time")



#login and browser


#
# --- force downloads to a known folder (works on macOS & Windows) ---
DOWNLOAD_DIR = os.path.abspath(os.path.join(os.getcwd(), 'artifacts', 'downloads'))
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

options = webdriver.ChromeOptions()
options.add_experimental_option('prefs', {
    'download.default_directory': DOWNLOAD_DIR,           # absolute path required
    'download.prompt_for_download': False,                # don't show the Save dialog
    'download.directory_upgrade': True,
    'safebrowsing.enabled': True
})

driver = webdriver.Chrome(options=options)



#----end helper for download--------
# --- wait for file to appear in the configured download folder ---
try:
    saved_file = wait_for_download(DOWNLOAD_DIR, timeout=120)
    print(f"✅ Download completed: {saved_file}")
except TimeoutError as e:
    print(f"❌ {e}")