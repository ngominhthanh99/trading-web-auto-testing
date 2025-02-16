from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from src.utils.constants import (
OPEN_POSITION, EDIT_POSITION, EDIT_POSITION_UPDATE, EDIT_POSITION_UPDATE_CONFIRM
)

def edit_open_position(driver):
    try:
        openposition = driver.find_element(By.CSS_SELECTOR, OPEN_POSITION)
        openposition.click()
    
        button_edit = driver.find_element(By.CSS_SELECTOR, EDIT_POSITION)
        button_edit.click()
        time.sleep(1)
    
        editSL = driver.find_element(By.CSS_SELECTOR, "[data-testid='edit-input-stoploss-price-decrease']")
        for _ in range(20):
            editSL.click()
        print("Order confirmed.")

        confirm_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, EDIT_POSITION_UPDATE)))
        confirm_button.click()
        
        confirm_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, EDIT_POSITION_UPDATE_CONFIRM)))
        confirm_button.click()
        
        print("Order confirmed.")
    
    except Exception as e:
        print(f"Error placing edit_open_position order: {e}")
    raise