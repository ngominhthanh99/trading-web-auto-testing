from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from src.driver_setup import setup_driver
from src.login import login
from src.utils.search_utils import search
from src.utils.price_utils import get_last_price
from src.orders import place_order
from src.utils.constants import TEST_SYMBOL, TEST_ORDER_UNITS, PLACE_ORDER_BUTTON

def test_place_market_order(driver):
    """Tests Market order."""
    try:   
        # Search for symbol
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

        # Place BUY MARKET order with SL and TP
        buy_stop_loss = last_price * 0.5  # 50% of last price
        buy_take_profit = last_price * 1.5  # 150% of last price
        place_order(driver, "BUY MARKET", TEST_ORDER_UNITS, stop_loss=buy_stop_loss, take_profit=buy_take_profit)
        time.sleep(5)

        # Place SELL MARKET order with SL and TP
        sell_stop_loss = last_price * 1.5  # 150% of last price
        sell_take_profit = last_price * 0.5  # 50% of last price
        place_order(driver, "SELL MARKET", TEST_ORDER_UNITS, stop_loss=sell_stop_loss, take_profit=sell_take_profit)

    except Exception as e:
        print(f"Error in test_place_market_order: {e}")
        raise