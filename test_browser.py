from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time

options = Options()
options.add_argument('--disable-gpu')
# ↓ 表示させたい場合 headlessは使わない
# options.add_argument('--headless')

# ChromeDriverをこのファイルと同じ場所から取得
driver_path = os.path.join(os.path.dirname(__file__), "chromedriver.exe")
service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=options)

driver.get("https://www.doubutsu-uranai.com/animal/")

try:
    # name="year" のselectが現れるまで20秒待つ
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.NAME, "year"))
    )
    print("フォームが表示されました！")
except:
    print("フォームが表示されませんでした…")

time.sleep(100)
driver.quit()
