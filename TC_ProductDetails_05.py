import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


chrome_options = Options()
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
)

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=chrome_options
)

driver.maximize_window()
wait = WebDriverWait(driver, 20)

try:
    print("STEP 1: Opening Amazon homepage")
    driver.get("https://www.amazon.com")

    print("STEP 2: Searching for product 'NVIDIA RTX 5070'")
    search_box = wait.until(
        EC.presence_of_element_located((By.ID, "twotabsearchtextbox"))
    )
    search_box.clear()
    search_box.send_keys("NVIDIA RTX 5070")
    search_box.send_keys(Keys.ENTER)

    time.sleep(3)

    print("STEP 3: Clicking first product from search results")

    first_product = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "a.a-link-normal.s-no-outline")
        )
    )

    driver.execute_script(
        "arguments[0].scrollIntoView({block:'center'});",
        first_product
    )
    time.sleep(1)
    driver.execute_script("arguments[0].click();", first_product)

    if len(driver.window_handles) > 1:
        driver.switch_to.window(driver.window_handles[1])

    time.sleep(3)

    print("STEP 4: Scrolling down product detail page")

    current_position = 0
    page_height = driver.execute_script("return document.body.scrollHeight")

    while current_position < page_height:
        current_position += 350
        driver.execute_script(f"window.scrollTo(0, {current_position});")
        time.sleep(0.6)
        page_height = driver.execute_script("return document.body.scrollHeight")

    print("✅ Test Passed: Search, product click, and product page scrolling completed successfully")

except Exception as e:
    print(f"❌ Test Failed due to error: {e}")
    driver.save_screenshot("debug_error.png")

finally:
    time.sleep(5)
    driver.quit()
