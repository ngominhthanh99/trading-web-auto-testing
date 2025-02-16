from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from src.utils.constants import BULK_DELETE, BULK_DELETE_CONFIRM
from src.utils.constants import PENDING_POSITION


def test_bulk_delete(driver):
    try:
        pendingposition = driver.find_element(By.CSS_SELECTOR, PENDING_POSITION)
        pendingposition.click()

        bulk_delete = driver.find_element(By.CSS_SELECTOR, BULK_DELETE)
        bulk_delete.click()

        # Click the Confirm button in the confirmation pop-up
        confirm_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, BULK_DELETE_CONFIRM)))
        confirm_button.click()
        time.sleep(5)



    except Exception as e:
        print(f"Error placing {test_bulk_delete} order: {e}")
        raise    
