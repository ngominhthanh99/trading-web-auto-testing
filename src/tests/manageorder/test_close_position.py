from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.utils.constants import CLOSE_POSITION_BUTTON, CLOSE_ORDER_CONFIRM_BUTTON
from src.utils.validation_utils import validate_order_history
import time

def test_close_position(driver):
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, CLOSE_POSITION_BUTTON))).click()

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, CLOSE_ORDER_CONFIRM_BUTTON))).click()
  
    except Exception as e:
        print(f"Error in test_close_position: {e}")
        raise