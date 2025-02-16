from src.driver_setup import setup_driver
from src.login import login
from src.tests.test_market_order import test_place_market_order
from src.tests.test_limit_order import test_place_limit_order
from src.tests.test_stop_order import test_place_stop_order
from src.tests.test_close_position import test_close_position
from src.tests.test_bulk_close import test_bulk_close
from src.tests.test_bulk_delete import test_bulk_delete
from src.tests.test_edit_open_position import edit_open_position
from src.tests.test_partial_close import test_patial_close
from src.tests.test_edit_pending_order import test_edit_pending_order
import time

def main():
    """Execute automation steps."""
    driver = setup_driver()
    
    try:
        # Log in
        login(driver)
        time.sleep(1)

        # Test market order and notification, open position validation
        test_place_market_order(driver)
        time.sleep(5)

        # Test limit order and notification, open position validation
        test_place_limit_order(driver)
        time.sleep(5)

        # Test stop order and notification, open position validation
        test_place_stop_order(driver)
        time.sleep(5)

        # Test edit open position
        edit_open_position(driver)
        time.sleep(5)

        # Test partal close
        test_patial_close(driver)
        time.sleep(5)

        # Test close position
        test_close_position(driver)
        time.sleep(5)

        #Test edit pending order
        test_edit_pending_order(driver)
        time.sleep(5)

        #Test bulk delete
        test_bulk_delete(driver)
        time.sleep(5)

        #Test bulk clsoe
        test_bulk_close(driver)
        time.sleep(5)

    except Exception as e:
        print(f"Unexpected error in main execution: {e}")

    finally:
        print("Closing browser...")
        driver.quit()

if __name__ == "__main__":
    main()