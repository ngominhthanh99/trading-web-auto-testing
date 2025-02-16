from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from .constants import (
    ORDER_TYPE_DROPDOWN, MARKET_ORDER_OPTION, STOP_ORDER_OPTION, LIMIT_ORDER_OPTION,
    VOLUME_INPUT, PRICE_INPUT, STOP_LOSS_INPUT, TAKE_PROFIT_INPUT, PLACE_ORDER_BUTTON,
    CONFIRM_BUTTON, EXPIRY_DROPDOWN, SELL_BUTTON, BUY_BUTTON, TRADE_VOLUME_INFO,
    GOOD_TILL_CANCELLED, GOOD_TILL_DAY
)
import time
from .validation_utils import validate_notification
from src.models.order import Order

def place_order(driver, order: Order):
    """Places an order with the given parameters."""
    try:
        # Determine Buy/Sell
        if "SELL" in order.order_type:
            driver.find_element(By.CSS_SELECTOR, SELL_BUTTON).click()
        else:
            driver.find_element(By.CSS_SELECTOR, BUY_BUTTON).click()
        
        # Select Order Type
        order_type_dropdown = driver.find_element(By.CSS_SELECTOR, ORDER_TYPE_DROPDOWN)
        order_type_dropdown.click()
        
        if "LIMIT" in order.order_type:
            driver.find_element(By.CSS_SELECTOR, LIMIT_ORDER_OPTION).click()
        elif "STOP" in order.order_type:
            driver.find_element(By.CSS_SELECTOR, STOP_ORDER_OPTION).click()
        else:
            driver.find_element(By.CSS_SELECTOR, MARKET_ORDER_OPTION).click()
        
        # Enter Units
        units_input = driver.find_element(By.CSS_SELECTOR, VOLUME_INPUT)
        units_input.send_keys(Keys.CONTROL + "a")
        units_input.send_keys(Keys.DELETE)
        units_input.send_keys(order.units)
        
        # Enter Price if applicable
        if order.price is not None:
            price_input = driver.find_element(By.CSS_SELECTOR, PRICE_INPUT)
            price_input.clear()
            price_input.send_keys(str(order.price))
        
        # Enter Stop Loss if applicable
        if order.stop_loss is not None:
            stop_loss_input = driver.find_element(By.CSS_SELECTOR, STOP_LOSS_INPUT)
            stop_loss_input.clear()
            stop_loss_input.send_keys(str(order.stop_loss))
        
        # Enter Take Profit if applicable
        if order.take_profit is not None:
            take_profit_input = driver.find_element(By.CSS_SELECTOR, TAKE_PROFIT_INPUT)
            take_profit_input.clear()
            take_profit_input.send_keys(str(order.take_profit))
        
        # Select Expiry if applicable
        if order.expiry is not None:
            
            expiry_dropdown = driver.find_element(By.CSS_SELECTOR, EXPIRY_DROPDOWN)
            expiry_dropdown.click()
            if order.expiry == "Good Till Cancelled":
                expiry_option = driver.find_element(By.CSS_SELECTOR, GOOD_TILL_CANCELLED)
            else:
                expiry_option = driver.find_element(By.CSS_SELECTOR, GOOD_TILL_DAY)
            expiry_option.click()
        
        order.size = driver.find_element(By.CSS_SELECTOR, TRADE_VOLUME_INFO).text
        print(f"Placing {order.order_type} order with Units = {order.units}, Size = {order.size}, Price = {order.price}, Stop Loss = {order.stop_loss}, Take Profit = {order.take_profit}, Expiry = {order.expiry}.")
        
        # Place Order
        place_order_button = driver.find_element(By.CSS_SELECTOR, PLACE_ORDER_BUTTON)
        place_order_button.click()
        
        # Click the Confirm button in the confirmation pop-up
        confirm_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, CONFIRM_BUTTON)))
        confirm_button.click()
        
        print("Order confirmed.")

        time.sleep(1)

        # Validate notification
        validate_notification(driver, order)
    
    except Exception as e:
        print(f"Error placing {order.order_type} order: {e}")
        raise