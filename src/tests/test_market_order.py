from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from src.utils.search_utils import search
from src.utils.price_utils import get_live_price
from src.utils.orders_utils import place_order
from src.utils.constants import TEST_SYMBOL, PLACE_ORDER_BUTTON, SYMBOL_ID

def test_place_market_order(driver):
    """Tests Market order."""
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

        # Place BUY MARKET order with SL and TP
        buy_stop_loss = round(get_live_price(driver, "true") * 0.5, 2)  # 50% of last price
        buy_take_profit = round(get_live_price(driver, "true") * 1.5, 2)  # 150% of last price
        place_order(driver, TEST_SYMBOL, "BUY", "1", stop_loss=buy_stop_loss, take_profit=buy_take_profit)

        time.sleep(3)

        # Place SELL MARKET order with SL and TP
        sell_stop_loss = round(get_live_price(driver, "false") * 1.5, 2)  # 150% of last price
        sell_take_profit = round(get_live_price(driver, "false") * 0.5, 2)  # 50% of last price
        place_order(driver, TEST_SYMBOL, "SELL", "0.5", stop_loss=sell_stop_loss, take_profit=sell_take_profit)

    except Exception as e:
        print(f"Error in test_place_market_order: {e}")
        raise