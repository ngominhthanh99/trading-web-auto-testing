from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from src.utils.search_utils import search
from src.utils.price_utils import get_live_price
from src.orders import place_order
from src.utils.constants import TEST_SYMBOL, GOOD_TILL_CANCELLED, GOOD_TILL_DAY, PLACE_ORDER_BUTTON, SYMBOL_ID

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

        # Place BUY STOP order with no SL nor TP and expiry Good Till Cancelled
        buy_stop_price = get_live_price(driver, "true") * 1.1
        place_order(driver, "BUY STOP", "1", price=buy_stop_price, expiry=GOOD_TILL_CANCELLED)
        
        time.sleep(5)

        # Place BUY STOP order with SL and TP and expiry Good Till Cancelled
        buy_stop_price = get_live_price(driver, "true") * 1.1
        place_order(driver, "BUY STOP", "2", price=buy_stop_price, stop_loss=buy_stop_price*0.5, take_profit=buy_stop_price*1.1, expiry=GOOD_TILL_CANCELLED)
        
        time.sleep(5)

        # Place BUY STOP order with no SL nor TP and expiry Good Till Day
        buy_stop_price = get_live_price(driver, "true") * 1.1
        place_order(driver, "BUY STOP", "1", price=buy_stop_price, expiry=GOOD_TILL_DAY)
        
        time.sleep(5)

        # Place BUY STOP order with SL and TP and expiry Good Till Day
        buy_stop_price = get_live_price(driver, "true") * 1.1
        place_order(driver, "BUY STOP", "2", price=buy_stop_price, stop_loss=buy_stop_price*0.5, take_profit=buy_stop_price*1.1, expiry=GOOD_TILL_DAY)
        
        time.sleep(5)

        # Place SELL STOP order with no SL nor TP and expiry Good Till Cancelled
        sell_stop_price = get_live_price(driver, "false") * 0.9
        place_order(driver, "SELL STOP", "1", price=sell_stop_price, expiry=GOOD_TILL_CANCELLED)
        
        time.sleep(5)

        # Place SELL STOP order with SL and TP and expiry Good Till Cancelled
        sell_stop_price = get_live_price(driver, "false") * 0.9
        place_order(driver, "SELL STOP", "2", price=sell_stop_price, stop_loss=sell_stop_price*1.1, take_profit=sell_stop_price*0.5, expiry=GOOD_TILL_CANCELLED)
        
        time.sleep(5)

        # Place SELL STOP order with no SL nor TP and expiry Good Till Day
        sell_stop_price = get_live_price(driver, "false") * 0.9
        place_order(driver, "SELL STOP", "0.2", price=sell_stop_price, expiry=GOOD_TILL_DAY)
        
        time.sleep(5)

        # Place SELL STOP order with SL and TP and expiry Good Till Day
        sell_stop_price = get_live_price(driver, "false") * 0.9
        place_order(driver, "SELL STOP", "2", price=sell_stop_price, stop_loss=sell_stop_price*1.1, take_profit=sell_stop_price*0.5, expiry=GOOD_TILL_DAY)

    except Exception as e:
        print(f"Error in test_place_stop_order: {e}")
        raise