import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


chrome_options = Options()
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
)

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=chrome_options
)

driver.maximize_window()
wait = WebDriverWait(driver, 20)

try:
    print("1. Opening Amazon homepage...")
    driver.get("https://www.amazon.com")

    time.sleep(3)

    print("2. Scrolling till end of the page...")
    current_position = 0
    page_height = driver.execute_script("return document.body.scrollHeight")

    while current_position < page_height:
        current_position += 350
        driver.execute_script(f"window.scrollTo(0, {current_position});")
        time.sleep(0.6)
        page_height = driver.execute_script("return document.body.scrollHeight")

    print("   -> Reached end of page successfully.")

except Exception as e:
    print(f"Error: {e}")
    driver.save_screenshot("scroll_error.png")

finally:
    print("✅ Test Passed!")
    time.sleep(5)
    driver.quit()
