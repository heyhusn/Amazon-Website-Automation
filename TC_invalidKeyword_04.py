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

wait = WebDriverWait(driver, 10)

search_box = wait.until(
    EC.presence_of_element_located((By.ID, "twotabsearchtextbox"))
)

invalid_keyword = "*%ksjd%&@#@(@323903^320hfkjshdfkjsd"
search_box.send_keys(invalid_keyword)
search_box.send_keys(Keys.ENTER)

try:
    no_results_message = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//*[contains(text(), 'No results for')]")
        )
    )
    print("✅TEST PASSED: 'No results' message was displayed successfully.")

except Exception:
    print(
        "TEST FAILED: The 'No results' message did not appear "
        "(or products were found unexpectedly)."
    )

# Stay for video evidence
time.sleep(5)
driver.quit()
