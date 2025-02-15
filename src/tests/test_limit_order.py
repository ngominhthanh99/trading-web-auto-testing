from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from src.driver_setup import setup_driver
from src.login import login
from src.utils.search_utils import search
from src.utils.price_utils import get_last_price
from src.orders import place_order
from src.utils.constants import TEST_SYMBOL, TEST_ORDER_UNITS, GOOD_TILL_CANCELLED, GOOD_TILL_DAY, PLACE_ORDER_BUTTON

def test_place_limit_order(driver):
    """Tests Limit order."""
    try:
        # Search for LTCUSD.std
        search(driver, TEST_SYMBOL)
        
        # Wait for the trade panel to load
        place_order_button = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, PLACE_ORDER_BUTTON))
        )

        # Check if the Place Order button is disabled
        is_disable = place_order_button.get_attribute("disabled")
        if is_disable == 'true':
            symbol = driver.find_element(By.CSS_SELECTOR, "[data-testid='symbol-overview-id']").text
            raise Exception(f"{symbol}: Market Closed")
        
        # Get the last price
        last_price = get_last_price(driver)

        # Place BUY LIMIT order
        buy_limit_price = last_price * 0.9  # 90% of last price
        place_order(driver, "BUY LIMIT", TEST_ORDER_UNITS, price=buy_limit_price, expiry=GOOD_TILL_CANCELLED)
        time.sleep(5)

        # Place SELL LIMIT order
        sell_limit_price = last_price * 1.10  # 110% of last price
        place_order(driver, "SELL LIMIT", TEST_ORDER_UNITS, price=sell_limit_price, expiry=GOOD_TILL_DAY)

    except Exception as e:
        print(f"Error in test_place_limit_order: {e}")
        raise