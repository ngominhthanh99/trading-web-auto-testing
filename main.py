from src.driver_setup import setup_driver
from src.login import login
from src.tests.test_market_order import test_place_market_order
from src.tests.test_limit_order import test_place_limit_order
from src.tests.test_stop_order import test_place_stop_order
import time

def main():
    """Execute automation steps."""
    driver = setup_driver()
    
    try:
        # Log in
        login(driver)
        time.sleep(5)

        # Test market order
        test_place_market_order(driver)
        time.sleep(5)

        # Test limit order
        test_place_limit_order(driver)
        time.sleep(5)

        # Test stop order
        test_place_stop_order(driver)

    except Exception as e:
        print(f"Unexpected error in main execution: {e}")

    finally:
        print("Closing browser...")
        driver.quit()

if __name__ == "__main__":
    main()