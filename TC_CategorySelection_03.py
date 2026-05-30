from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
import time


chrome_options = Options()
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=chrome_options
)

driver.maximize_window()

driver.get("https://www.amazon.com")
wait = WebDriverWait(driver, 15)

try:
    dropdown_element = wait.until(
        EC.presence_of_element_located((By.ID, "searchDropdownBox"))
    )

    select = Select(dropdown_element)

    TARGET_CATEGORY = "Books"

    print(f"Attempting to select category: '{TARGET_CATEGORY}'...")
    select.select_by_visible_text(TARGET_CATEGORY)

    selected_option = select.first_selected_option.text.strip()

    if selected_option == TARGET_CATEGORY:
        print(f"✅TEST PASSED: Category '{selected_option}' was selected successfully.")
    else:
        print(f"TEST FAILED: Expected '{TARGET_CATEGORY}', but found '{selected_option}'.")

    search_box = driver.find_element(By.ID, "twotabsearchtextbox")
    search_box.send_keys("Harry Potter")
    search_box.send_keys(Keys.ENTER)

    wait.until(EC.presence_of_element_located((By.ID, "search")))

    current_position = 0
    page_height = driver.execute_script("return document.body.scrollHeight")

    while current_position < page_height:
        current_position += 400
        driver.execute_script(f"window.scrollTo(0, {current_position});")
        time.sleep(0.6)
        page_height = driver.execute_script("return document.body.scrollHeight")

    if "books" in driver.current_url.lower() or "books" in driver.title.lower():
        print("✅TEST PASSED: Search was successfully executed within the 'Books' category.")
    else:
        print("WARNING: Category selected, but URL/title does not clearly show 'Books'. Check manually.")

except Exception as e:
    print(f"TEST FAILED: An error occurred - {e}")

finally:
    time.sleep(3)
    driver.quit()
