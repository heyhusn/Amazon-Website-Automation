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
    product_url = f"https://www.amazon.com/dp/{TARGET_ASIN}"

    print(f"1. Opening product page: {product_url}")
    driver.get(product_url)

    try:
        one_time_purchase_box = driver.find_element(By.CSS_SELECTOR, "i.a-icon-radio-inactive")
        one_time_purchase_box.click()
        time.sleep(1)
        print("Selected 'One-time purchase'.")
    except:
        print("No 'Subscribe & Save' toggle found, proceeding...")

    print("2. Looking for 'Add to Cart' button...")

    try:
        add_to_cart_btn = wait.until(
            EC.element_to_be_clickable((By.ID, "add-to-cart-button"))
        )
    except:
        add_to_cart_btn = driver.find_element(By.NAME, "submit.add-to-cart")

    add_to_cart_btn.click()
    print("3. Button clicked.")

    try:
        no_thanks_btn = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "#attachSiNoCoverage span input")
            )
        )
        no_thanks_btn.click()
        print("Dismissed Warranty Pop-up.")
    except:
        pass

    print("4. Verifying cart update...")
    wait.until(lambda d: d.find_element(By.ID, "nav-cart-count").text != "0")

    cart_count = driver.find_element(By.ID, "nav-cart-count").text
    print(f"5. Current Cart Count: {cart_count}")

    if int(cart_count) > 0:
        print("✅TEST PASSED: Item successfully added to cart.")
    else:
        print("TEST FAILED: Cart count is still 0.")

except Exception as e:
    print(f"Error occurred: {e}")
    driver.save_screenshot("cart_error.png")

finally:
    time.sleep(5)
    driver.quit()
