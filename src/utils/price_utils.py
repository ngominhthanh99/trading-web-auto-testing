from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_last_price(driver):
    """Gets last price from trade page."""
    try:
        # Wait for element to load
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".sc-ey6wxa-3 .sc-2l74dl-0")))
        
        # Get last price from element's text
        last_price_element = driver.find_element(By.CSS_SELECTOR, ".sc-ey6wxa-3 .sc-2l74dl-0")
        last_price_text = last_price_element.text
        last_price = float(last_price_text.replace(",", "").replace("$", ""))
        return last_price

    except Exception as e:
        print(f"Error retrieving last price: {e}")
        raise