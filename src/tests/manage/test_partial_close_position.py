from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.utils.constants import (CLOSE_POSITION_BUTTON, CLOSE_ORDER_CONFIRM_BUTTON, CLOSE_ORDER_VOLUME_DECREASE)
from src.utils.validation_utils import validate_order_history
import time

def test_patial_close(driver):
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(driver.find_element(By.CSS_SELECTOR, CLOSE_POSITION_BUTTON))).click()

        button_close_order_volume = driver.find_element(By.CSS_SELECTOR, CLOSE_ORDER_VOLUME_DECREASE)
        for _ in range(5):
            button_close_order_volume.click()

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, CLOSE_ORDER_CONFIRM_BUTTON))).click()
  
    except Exception as e:
        print(f"Error in test_patial_close: {e}")
        raise