from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

from src.utils.constants import CLOSE_POSITION_BUTTON, CLOSE_ORDER_POSITION

def test_close_position(driver):
    try:
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, CLOSE_POSITION_BUTTON))).click()
       
        button_close_order = driver.find_element(By.CSS_SELECTOR, CLOSE_ORDER_POSITION)
        button_close_order.click()
  
    except Exception as e:
        print(f"Error in test_close_position: {e}")
        raise