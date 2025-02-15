from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from src.utils.constants import (NOTIFICATION_BOX, NOTIFICATION_TITLE, NOTIFICATION_DESCRIPTION,
                                 BEARER_TOKEN, ORDER_API_ENDPOINT, PENDING_ORDER_API_ENDPOINT)

def validate_notifications(driver, symbol, order_type, size, units, price, stop_loss, take_profit):
    """Validate order details with notification."""
    try:
        # Wait for the notification pop-up to appear
        WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, NOTIFICATION_BOX)))

        notification_title, notification_description = get_notification_details(driver)
        print(f"Notification - Title: {notification_title}. Description: {notification_description}")

        if notification_description:
            # Fetch the latest order from the API
            latest_order = fetch_latest_order(symbol, order_type)
            if not latest_order:
                return

            api_order_type = map_order_type(latest_order.get("orderType"))

            validation_passed = compare_order_details(
                latest_order, symbol, order_type, size, units, price, stop_loss, take_profit, api_order_type
            )

            if validation_passed:
                print("Validation passed: All fields match the API response.")

    except Exception as e:
        print(f"Error validating notifications: {e}")
        raise

def get_notification_details(driver):
    """Get the notification title and description."""
    notification_title_element = driver.find_elements(By.CSS_SELECTOR, NOTIFICATION_TITLE)
    notification_description_element = driver.find_elements(By.CSS_SELECTOR, NOTIFICATION_DESCRIPTION)

    notification_title = notification_title_element[0].text if notification_title_element else ""
    notification_description = notification_description_element[0].text if notification_description_element else ""

    return notification_title, notification_description

def fetch_latest_order(symbol, order_type):
    """Fetch the latest order from the API."""
    api_url = PENDING_ORDER_API_ENDPOINT + symbol
    if order_type in ["BUY", "SELL"]:
        api_url = ORDER_API_ENDPOINT + symbol

    headers = {
        "Authorization": "Bearer " + BEARER_TOKEN,
        "Content-Type": "application/json"
    }

    response = requests.get(api_url, headers=headers)

    if response.status_code == 401:
        print("Error: Unauthorized. Please check your Bearer Token.")
        return None
    elif response.status_code != 200:
        print(f"Failed to fetch orders from API. Status code: {response.status_code}")
        return None

    orders = response.json().get("result", [])
    if not orders:
        print("No orders found in the API response.")
        return None

    return orders[0]  # Return the most recent order

def map_order_type(api_order_type):
    """Map API order type to human-readable format."""
    order_type_mapping = {
        0: "BUY",
        1: "SELL",
        2: "BUY LIMIT",
        3: "SELL LIMIT",
        4: "BUY STOP",
        5: "SELL STOP"
    }
    return order_type_mapping.get(api_order_type, "UNKNOWN")

def compare_order_details(latest_order, symbol, order_type, size, units, price, stop_loss, take_profit, api_order_type):
    """Compare API values with order details and return True if all match."""
    validation_passed = True

    # Extract details from the API response
    api_symbol = latest_order.get("symbol")
    api_units = latest_order.get("units")
    api_size = latest_order.get("lotSize")
    api_open_price = latest_order.get("openPrice")
    api_take_profit = latest_order.get("takeProfit")
    api_stop_loss = latest_order.get("stopLoss")

    # Compare each field
    if api_symbol != symbol:
        print(f"Wrong Symbol: Expected {symbol}, Found {api_symbol}")
        validation_passed = False

    if api_order_type != order_type:
        print(f"Wrong Type: Expected {order_type}, Found {api_order_type}")
        validation_passed = False

    if api_units != float(units):
        print(f"Wrong Units: Expected {units}, Found {api_units}")
        validation_passed = False

    if api_size != float(size):
        print(f"Wrong Size: Expected {size}, Found {api_size}")
        validation_passed = False

    if api_open_price is not None and price is not None:
        if abs(api_open_price - price) > 0.01:
            print(f"Wrong Price: Expected {price:.2f}, Found {api_open_price:.2f}")
            validation_passed = False

    if api_take_profit is not None and take_profit is not None:
        if abs(api_take_profit - take_profit) > 0.01:
            print(f"Wrong Take Profit: Expected {take_profit:.2f}, Found {api_take_profit:.2f}")
            validation_passed = False

    if api_stop_loss is not None and stop_loss is not None:
        if abs(api_stop_loss - stop_loss) > 0.01:
            print(f"Wrong Stop Loss: Expected {stop_loss:.2f}, Found {api_stop_loss:.2f}")
            validation_passed = False

    return validation_passed