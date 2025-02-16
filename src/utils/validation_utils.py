from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import requests
from .constants import (NOTIFICATION_BOX, NOTIFICATION_TITLE, NOTIFICATION_DESCRIPTION, OPEN_POSITIONS_API_URL, BEARER_TOKEN,
                        ORDER_HISTORY_API_URL, OPEN_POSITIONS_TABLE, ORDER_HISTORY_TABLE, OPEN_POSITIONS_TAB, ORDER_HISTORY_TAB)
from src.models.order import Order
from datetime import datetime, time
from datetime import datetime, time, timezone

def validate_notification(driver, order: Order):
    """Validate order details with notification."""
    try:
        # Wait for notification pop-up to appear
        WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, NOTIFICATION_BOX)))

        notification_title, notification_description = get_notification_details(driver)
        print(f"Notification - Title: {notification_title}. Description: {notification_description}")

        if notification_description:   
            validation_passed = compare_notification_with_order_details(notification_description, order)

            if validation_passed:
                print("Validation passed: notification matched with order details.")

    except Exception as e:
        print(f"Error validating notifications: {e}")
        raise

def validate_open_position(driver, order: Order):
    """Validate order details with open positions table."""
    try:
        # Click on Open Positions
        driver.find_element(By.CSS_SELECTOR, OPEN_POSITIONS_TAB).click()

        # Wait for open positions table to appear
        WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, OPEN_POSITIONS_TABLE)))

        api_url = OPEN_POSITIONS_API_URL + "?symbol=" + order.symbol

        latest_order = fetch_latest_order(api_url, BEARER_TOKEN, 0)
        if not latest_order:
            return
        
        validation_passed = compare_api_response_with_order_details(latest_order, order)

        if validation_passed:
                print("Validation passed: open position matched with order details.")

    except Exception as e:
        print(f"Error validating open position: {e}")
        raise

def validate_order_history(driver, order: Order):
    """Validate order details with order history data."""
    try:
        # Click on Order History
        driver.find_element(By.CSS_SELECTOR, ORDER_HISTORY_TAB).click()

        # Wait for order history table to appear
        WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ORDER_HISTORY_TABLE)))

        # Get current daytime
        now = datetime.now(timezone.utc)
        start_of_day = datetime.combine(now.date(), time.min, tzinfo=timezone.utc)
        end_of_day = datetime.combine(now.date(), time.max, tzinfo=timezone.utc)
        start_timestamp = int(start_of_day.timestamp() * 1000)
        end_timestamp = int(end_of_day.timestamp() * 1000)

        api_url = ORDER_HISTORY_API_URL + "?to=" + str(end_timestamp) + "&from=" + str(start_timestamp) + "&type=ORDER"

        print(f"{api_url}")

        latest_order = fetch_latest_order(api_url, BEARER_TOKEN, 0)
        if not latest_order:
            return
        
        validation_passed = compare_api_response_with_order_details(latest_order, order)

        if validation_passed:
                print("Validation passed: open position matched with order details.")

    except Exception as e:
        print(f"Error validating open position: {e}")
        raise

def get_notification_details(driver):
    """Get the notification title and description."""
    notification_title_element = driver.find_elements(By.CSS_SELECTOR, NOTIFICATION_TITLE)
    notification_description_element = driver.find_elements(By.CSS_SELECTOR, NOTIFICATION_DESCRIPTION)

    notification_title = notification_title_element[0].text if notification_title_element else ""
    notification_description = notification_description_element[0].text if notification_description_element else ""

    return notification_title, notification_description

def compare_notification_with_order_details(message, order: Order):
    # Mapping of fields to their labels in notification
    labels = {
        "symbol": "",
        "size": "Size:",
        "units": "Units:",
        "price": "Price:",
        "stop_loss": "Stop Loss:",
        "take_profit": "Take Profit:"
    }
    try:
        result = True
        # Symbol
        noti_symbol = re.match(r"^[^.]+\.\w+", message).group(0)
        if noti_symbol != order.symbol:
            print(f"Wrong Symbol: Expected {order.symbol}, Found {noti_symbol}.")
            result = False

        # Order Type
        match = re.search(r" - ([A-Z ]+ ORDER)", message)
        noti_order_type = match.group(1).replace(" ORDER", "").strip() if match else None
        if noti_order_type != order.order_type:
            print(f"Wrong Order Type: Expect {order.order_type}, Found {noti_order_type}.")
            result = False

        # Other fields
        for key, value in order.__dict__.items():
            if key in ["symbol","order_type","expiry"] or value is None:
                continue

            label = labels.get(key)
            search_string = f"{label} {value}"

            # Check if search string exists in the notification
            if search_string not in message:
                match = re.search(f"{label} (\d+(\.\d+)?)", message)
                actual_value = match.group(1) if match else None
                print(f"Wrong {label}: Expected {value}, Found {actual_value}.")
                result = False

        return result
    
    except Exception as e:
        print(f"Error validating notification: {e}")
        raise

def fetch_latest_order(api_url, token, position):
    """Fetch the latest order from API."""
    # Build headers
    headers = {
        "Authorization": "Bearer " + token,
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

    return orders[position]  # Return the most recent order

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

def compare_api_response_with_order_details(latest_order, order: Order):
    """Compare API values with order details and return True if all match."""
    validation_passed = True

    # Extract details from the API response
    api_symbol = latest_order.get("symbol")
    api_units = latest_order.get("units")
    api_size = latest_order.get("lotSize")
    api_open_price = latest_order.get("openPrice")
    api_take_profit = latest_order.get("takeProfit")
    api_stop_loss = latest_order.get("stopLoss")
    api_order_type = map_order_type(latest_order.get("orderType"))

    # Compare each field
    if api_symbol != order.symbol:
        print(f"Wrong Symbol: Expected {order.symbol}, Found {api_symbol}")
        validation_passed = False

    if api_order_type != order.order_type:
        print(f"Wrong Order Type: Expected {order.order_type}, Found {api_order_type}")
        validation_passed = False

    if api_units != float(order.units):
        print(f"Wrong Units: Expected {order.units}, Found {api_units}")
        validation_passed = False

    if api_size != float(order.size):
        print(f"Wrong Size: Expected {order.size}, Found {api_size}")
        validation_passed = False

    if api_open_price is not None and order.price is not None:
        if abs(api_open_price - order.price) > 0.01:
            print(f"Wrong Price: Expected {order.price:.2f}, Found {api_open_price:.2f}")
            validation_passed = False

    if api_take_profit is not None and order.take_profit is not None:
        if abs(api_take_profit - order.take_profit) > 0.01:
            print(f"Wrong Take Profit: Expected {order.take_profit:.2f}, Found {api_take_profit:.2f}")
            validation_passed = False

    if api_stop_loss is not None and order.stop_loss is not None:
        if abs(api_stop_loss - order.stop_loss) > 0.01:
            print(f"Wrong Stop Loss: Expected {order.stop_loss:.2f}, Found {api_stop_loss:.2f}")
            validation_passed = False

    return validation_passed