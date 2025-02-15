from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .constants import (LIVE_BUY_PRICE, LIVE_SELL_PRICE)

def get_live_price(driver, is_buy):
    """Gets last price from trade page."""
    try:
        # Wait for element to load
        last_price_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(By.CSS_SELECTOR, LIVE_SELL_PRICE))
        if is_buy == 'true':
            last_price_element = driver.find_element(By.CSS_SELECTOR, LIVE_BUY_PRICE)

        # Get last price from element's text
        last_price = float(last_price_element.text)
        
        return last_price

    except Exception as e:
        print(f"Error retrieving last price: {e}")
        raise