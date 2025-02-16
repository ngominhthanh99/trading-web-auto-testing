from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from src.utils.search_utils import search
from src.utils.price_utils import get_live_price
from src.utils.orders_utils import place_order
from src.utils.constants import TEST_SYMBOL, PLACE_ORDER_BUTTON, SYMBOL_ID
from src.models.order import Order

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
        buy_stop_price = round(get_live_price(driver, "true") * 1.1, 2)
        place_order(driver, Order(TEST_SYMBOL, "BUY STOP", units="1", price=buy_stop_price, expiry="Good Till Cancelled"))
        
        time.sleep(5)

        # Place BUY STOP order with SL and TP and expiry Good Till Cancelled
        buy_stop_price = round(get_live_price(driver, "true") * 1.1, 2)
        place_order(driver, Order(TEST_SYMBOL, "BUY STOP", units="2", price=buy_stop_price, stop_loss=round(buy_stop_price*0.5, 2), take_profit=round(buy_stop_price*1.1, 2), expiry="Good Till Cancelled"))
        
        time.sleep(5)

        # Place BUY STOP order with no SL nor TP and expiry Good Till Day
        buy_stop_price = round(get_live_price(driver, "true") * 1.1, 2)
        place_order(driver, Order(TEST_SYMBOL, "BUY STOP", units="1", price=buy_stop_price, expiry="Good Till Day"))
        
        time.sleep(5)

        # Place BUY STOP order with SL and TP and expiry Good Till Day
        buy_stop_price = round(get_live_price(driver, "true") * 1.1, 2)
        place_order(driver, Order(TEST_SYMBOL, "BUY STOP", units="2", price=buy_stop_price, stop_loss=round(buy_stop_price*0.5, 2), take_profit=round(buy_stop_price*1.1, 2), expiry="Good Till Day"))
        
        time.sleep(5)

        # Place SELL STOP order with no SL nor TP and expiry Good Till Cancelled
        sell_stop_price = round(get_live_price(driver, "false") * 0.9, 2)
        place_order(driver, Order(TEST_SYMBOL, "SELL STOP", units="1", price=sell_stop_price, expiry="Good Till Cancelled"))
        
        time.sleep(5)

        # Place SELL STOP order with SL and TP and expiry Good Till Cancelled
        sell_stop_price = round(get_live_price(driver, "false") * 0.9, 2)
        place_order(driver, Order(TEST_SYMBOL, "SELL STOP", units="2", price=sell_stop_price, stop_loss=round(sell_stop_price*1.1, 2), take_profit=round(sell_stop_price*0.5, 2), expiry="Good Till Cancelled"))
        
        time.sleep(5)

        # Place SELL STOP order with no SL nor TP and expiry Good Till Day
        sell_stop_price = round(get_live_price(driver, "false") * 0.9, 2)
        place_order(driver, Order(TEST_SYMBOL, "SELL STOP", units="0.2", price=sell_stop_price, expiry="Good Till Day"))
        
        time.sleep(5)

        # Place SELL STOP order with SL and TP and expiry Good Till Day
        sell_stop_price = round(get_live_price(driver, "false") * 0.9, 2)
        place_order(driver, Order(TEST_SYMBOL, "SELL STOP", units="2", price=sell_stop_price, stop_loss=round(sell_stop_price*1.1, 2), take_profit=round(sell_stop_price*0.5, 2), expiry="Good Till Day"))

    except Exception as e:
        print(f"Error in test_place_stop_order: {e}")
        raise