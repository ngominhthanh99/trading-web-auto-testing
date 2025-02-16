from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from src.utils.constants import (
OPEN_POSITIONS_TAB, EDIT_POSITION, EDIT_POSITION_UPDATE, EDIT_POSITION_UPDATE_CONFIRM, EDIT_STOPLOSS_DECREASE
)

def edit_open_position(driver):
    try:
        openposition = driver.find_element(By.CSS_SELECTOR, OPEN_POSITIONS_TAB)
        openposition.click()
        time.sleep(1)
    
        button_edit = driver.find_element(By.CSS_SELECTOR, EDIT_POSITION)
        button_edit.click()

    
        editSL = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, EDIT_STOPLOSS_DECREASE)))
        for _ in range(10):
            editSL.click()
        print("Edit confirmed.")


        confirm_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, EDIT_POSITION_UPDATE)))
        confirm_button.click()
        
        confirm_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, EDIT_POSITION_UPDATE_CONFIRM)))
        confirm_button.click()
        
        print("Edit confirmed.")
    
    except Exception as e:
        print(f"Error in edit_open_position order: {e}")
        raise