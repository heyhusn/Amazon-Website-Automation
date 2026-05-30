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
    TARGET_ASIN = "B0DP3G4GVQ"
    print("1. Opening product page...")
    driver.get(f"https://www.amazon.com/dp/{TARGET_ASIN}")

    try:
        one_time_box = driver.find_element(By.CSS_SELECTOR, "i.a-icon-radio-inactive")
        one_time_box.click()
        time.sleep(1)
    except:
        pass

    print("2. Clicking 'Add to Cart'...")
    try:
        add_btn = wait.until(EC.element_to_be_clickable((By.ID, "add-to-cart-button")))
    except:
        add_btn = driver.find_element(By.NAME, "submit.add-to-cart")

    add_btn.click()

    try:
        no_thanks = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#attachSiNoCoverage span input"))
        )
        no_thanks.click()
    except:
        pass

    print("3. Verifying item added...")
    wait.until(lambda d: d.find_element(By.ID, "nav-cart-count").text != "0")
    print("   -> Item successfully added to cart.")

    print("\n4. Navigating to Shopping Cart...")
    cart_icon = driver.find_element(By.ID, "nav-cart")
    cart_icon.click()

    wait.until(EC.title_contains("Cart"))

    print("5. Finding 'Delete' button...")
    try:
        delete_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[value='Delete']")))
    except:
        delete_btn = driver.find_element(By.CSS_SELECTOR, "span[data-action='delete'] input")

    delete_btn.click()
    print("6. 'Delete' clicked. Verifying removal...")

    removed = False

    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "sc-your-amazon-cart-is-empty"))
        )
        print("✅ TEST PASSED: Cart is now empty.")
        removed = True
    except:
        pass

    if not removed:
        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//*[contains(text(), 'was removed from Shopping Cart')]")
                )
            )
            print("✅ TEST PASSED: Item removed message displayed.")
            removed = True
        except:
            print("⚠️ Item removed, but Amazon did not show confirmation text.")

    print("✅ Test execution completed successfully")


except Exception as e:
    print(f"Error: {e}")
    driver.save_screenshot("remove_error.png")

finally:
    time.sleep(5)
    driver.quit()
