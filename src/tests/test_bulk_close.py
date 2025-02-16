from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from src.utils.constants import (BULK_CLOSE_DROPDOWN, BULK_CLOSE_ALL, 
BULK_CLOSE_LOSS, BULK_CLOSE_PROFIT, BULK_CLOSE_PROFIT_CONFIRM, 
BULK_CLOSE_LOSS_CONFIRM, BULK_CLOSE_ALL_CONFIRM, OPEN_POSITIONS_TAB
)



def test_bulk_close(driver):
    try:
        openposition = driver.find_element(By.CSS_SELECTOR, OPEN_POSITIONS_TAB)
        openposition.click()

        bulk_close = driver.find_element(By.CSS_SELECTOR, BULK_CLOSE_DROPDOWN)
        bulk_close.click()
    
        driver.find_element(By.CSS_SELECTOR, BULK_CLOSE_ALL).click()

        # Click the Confirm button in the confirmation pop-up
        confirm_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, BULK_CLOSE_ALL_CONFIRM)))
        confirm_button.click()
        time.sleep(5)
        print("Order confirmed.")

        driver.find_element(By.CSS_SELECTOR, BULK_CLOSE_PROFIT).click()
        
        # Click the Confirm button in the confirmation pop-up
        confirm_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, BULK_CLOSE_LOSS_CONFIRM)))
        confirm_button.click()
        time.sleep(5)
        print("Order confirmed.")

        driver.find_element(By.CSS_SELECTOR, BULK_CLOSE_LOSS).click()

        # Click the Confirm button in the confirmation pop-up
        confirm_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, BULK_CLOSE_PROFIT_CONFIRM)))
        confirm_button.click()
        time.sleep(5)
        print("Order confirmed.")
        
    
    except Exception as e:
        print(f"Error placing {test_bulk_close} order: {e}")
        raise