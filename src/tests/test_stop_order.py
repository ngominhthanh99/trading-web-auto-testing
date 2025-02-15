from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from src.driver_setup import setup_driver
from src.login import login
from src.utils.search_utils import search
from src.utils.price_utils import get_live_price
from src.orders import place_order
from src.utils.constants import TEST_SYMBOL, TEST_ORDER_UNITS, GOOD_TILL_CANCELLED, GOOD_TILL_DAY, PLACE_ORDER_BUTTON, SYMBOL_ID

def test_place_stop_order(driver):
    """Tests Stop order."""
    try:
        # Search for ticker symbol
        search(driver, TEST_SYMBOL)
        
        # Wait for trade panel to load
        place_order_button = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, PLACE_ORDER_BUTTON))
        )

        # Check if Place Order button is disabled
        is_disable = place_order_button.get_attribute("disabled")
        if is_disable == 'true':
            symbol = driver.find_element(By.CSS_SELECTOR, SYMBOL_ID).text
            raise Exception(f"{symbol}: Market Closed")

        # Place BUY STOP order
        buy_stop_price = get_live_price(driver, "true") * 1.10  # 110% of last price
        place_order(driver, "BUY STOP", TEST_ORDER_UNITS, price=buy_stop_price, expiry=GOOD_TILL_CANCELLED)

        time.sleep(5)

        # Place SELL STOP order
        sell_stop_price = get_live_price(driver, "false") * 0.9  # 90% of last price
        place_order(driver, "SELL STOP", TEST_ORDER_UNITS, price=sell_stop_price, expiry=GOOD_TILL_DAY)

    except Exception as e:
        print(f"Error in test_place_stop_order: {e}")
        raise