from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
from src.utils.constants import (
    PENDING_POSITIONS_TAB, EDIT_ORDER, EDIT_ORDER_UPDATE, EDIT_ORDER_UPDATE_CONFIRM,
    EDIT_GOOD_TILL_CANCELLED, EDIT_GOOD_TILL_DAY, EDIT_EXPIRY_DROPDOWN,
    EDIT_ORDER_PRICE_INPUT, EDIT_ORDER_SL_INPUT, EDIT_ORDER_TP_INPUT, EDIT_ORDER_SL_POINT, EDIT_ORDER_TP_POINT
)

new_price = 130.50 
new_stop_loss_price = 90.00  
new_stop_loss_points = 500  
new_take_profit_price = 210.00 
new_take_profit_points = 900  
new_expiry = 'Good Till Day'  


def test_edit_pending_order(driver):
    try:
        pendingposition = driver.find_element(By.CSS_SELECTOR, PENDING_POSITIONS_TAB)
        pendingposition.click()
        
        edit_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, EDIT_ORDER)))
        edit_button.click()
        print("Edit confirmed.")
    
        wait = WebDriverWait(driver, 10)
        price_field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, EDIT_ORDER_PRICE_INPUT)))
        price_field.clear()
        price_field.send_keys(str(new_price))

        # Locate and edit the "Stop Loss Price" field
        stop_loss_price_field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, EDIT_ORDER_SL_INPUT)))
        stop_loss_price_field.clear()
        stop_loss_price_field.send_keys(str(new_stop_loss_price))
        print("Edit confirmed.")

        # Locate and edit the "Stop Loss Points" field
        stop_loss_points_field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, EDIT_ORDER_SL_POINT )))
        stop_loss_points_field.send_keys(Keys.CONTROL + "a")
        stop_loss_points_field.send_keys(Keys.DELETE)
        stop_loss_points_field.send_keys(str(new_stop_loss_points))
        print("Edit confirmed.")

        # Locate and edit the "Take Profit Price" field
        take_profit_price_field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, EDIT_ORDER_TP_INPUT)))
        take_profit_price_field.clear()
        take_profit_price_field.send_keys(str(new_take_profit_price))
        print("Edit confirmed.")

        # Locate and edit the "Take Profit Points" field
        take_profit_points_field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, EDIT_ORDER_TP_POINT)))
        take_profit_points_field.send_keys(Keys.CONTROL + "a")
        take_profit_points_field.send_keys(Keys.DELETE)
        take_profit_points_field.send_keys(str(new_take_profit_points))

        expiry_dropdown = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, EDIT_EXPIRY_DROPDOWN)))
        expiry_dropdown.click()
        print("Edit confirmed.")

        # Select "Good Till Day" or "Good Till Cancelled" 
        if new_expiry == 'Good Till Day':
            expiry_option = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, EDIT_GOOD_TILL_DAY)))
        else:
            expiry_option = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, EDIT_GOOD_TILL_CANCELLED)))
            
        expiry_option.click()


        price_plus = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='edit-input-price-increase']")))
        for _ in range(20):
            price_plus.click()
        print("Edit confirmed.")


        update_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, EDIT_ORDER_UPDATE))
        )
        update_button.click()
        print("Edit confirmed.")

        # Click the Confirm button in the confirmation pop-up
        confirm_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, EDIT_ORDER_UPDATE_CONFIRM)))
        confirm_button.click()
        time.sleep(5)

    except Exception as e:
        print(f"Error in test_edit_pending_order: {e}")
        raise
