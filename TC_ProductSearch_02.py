from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time


driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install())
)
driver.maximize_window()

driver.get("https://www.amazon.com")

wait = WebDriverWait(driver, 15)

search_box = wait.until(
    EC.presence_of_element_located((By.ID, "twotabsearchtextbox"))
)

search_box.send_keys("wireless mouse")
search_box.send_keys(Keys.ENTER)

results = wait.until(
    EC.presence_of_all_elements_located(
        (By.CSS_SELECTOR, "div[data-component-type='s-search-result']")
    )
)

current_position = 0
page_height = driver.execute_script("return document.body.scrollHeight")

while current_position < page_height:
    current_position += 400
    driver.execute_script(f"window.scrollTo(0, {current_position});")
    time.sleep(0.6)
    page_height = driver.execute_script("return document.body.scrollHeight")

if len(results) > 0:
    print("✅TEST PASSED: Search results are displayed.")
else:
    print("TEST FAILED: No search results found.")

time.sleep(2)
driver.quit()
