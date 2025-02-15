from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.constants import (
    ORDER_TYPE_DROPDOWN, MARKET_ORDER_OPTION, STOP_ORDER_OPTION, LIMIT_ORDER_OPTION,
    VOLUME_INPUT, PRICE_INPUT, STOP_LOSS_INPUT, TAKE_PROFIT_INPUT, PLACE_ORDER_BUTTON,
    CONFIRM_BUTTON, EXPIRY_DROPDOWN, SELL_BUTTON, BUY_BUTTON, TRADE_VOLUME_INFO
)

def place_order(driver, order_type, units, price=None, stop_loss=None, take_profit=None, expiry=None):
    """Places an order with the given parameters."""
    try:
        # Determine Buy/Sell
        if "SELL" in order_type:
            driver.find_element(By.CSS_SELECTOR, SELL_BUTTON).click()
        else:
            driver.find_element(By.CSS_SELECTOR, BUY_BUTTON).click()
        
        # Select Order Type
        order_type_dropdown = driver.find_element(By.CSS_SELECTOR, ORDER_TYPE_DROPDOWN)
        order_type_dropdown.click()
        
        if "LIMIT" in order_type:
            driver.find_element(By.CSS_SELECTOR, LIMIT_ORDER_OPTION).click()
        elif "STOP" in order_type:
            driver.find_element(By.CSS_SELECTOR, STOP_ORDER_OPTION).click()
        else:
            driver.find_element(By.CSS_SELECTOR, MARKET_ORDER_OPTION).click()
        
        # Enter Units
        units_input = driver.find_element(By.CSS_SELECTOR, VOLUME_INPUT)
        units_input.clear()
        units_input.send_keys(units)
        
        # Enter Price if applicable
        if price is not None:
            price_input = driver.find_element(By.CSS_SELECTOR, PRICE_INPUT)
            price_input.clear()
            price_input.send_keys(str(price))
        
        # Enter Stop Loss if applicable
        if stop_loss is not None:
            stop_loss_input = driver.find_element(By.CSS_SELECTOR, STOP_LOSS_INPUT)
            stop_loss_input.clear()
            stop_loss_input.send_keys(str(stop_loss))
        
        # Enter Take Profit if applicable
        if take_profit is not None:
            take_profit_input = driver.find_element(By.CSS_SELECTOR, TAKE_PROFIT_INPUT)
            take_profit_input.clear()
            take_profit_input.send_keys(str(take_profit))
        
        # Select Expiry if applicable
        if expiry is not None:
            expiry_dropdown = driver.find_element(By.CSS_SELECTOR, EXPIRY_DROPDOWN)
            expiry_dropdown.click()
            expiry_option = driver.find_element(By.CSS_SELECTOR, expiry)
            expiry_option.click()
        
        size = driver.find_element(By.CSS_SELECTOR, TRADE_VOLUME_INFO).text
        print(f"Placing {order_type} order with Units = {units}, Size = {size}, Price = {price}, Stop Loss = {stop_loss}, Take Profit = {take_profit}, Expiry = {expiry}.")
        
        # Place Order
        place_order_button = driver.find_element(By.CSS_SELECTOR, PLACE_ORDER_BUTTON)
        place_order_button.click()
        
        # Click the Confirm button in the confirmation pop-up
        confirm_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(By.CSS_SELECTOR, CONFIRM_BUTTON))
        confirm_button.click()
        
        print("Order confirmed.")
    
    except Exception as e:
        print(f"Error placing {order_type} order: {e}")
        raise