from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
from .constants import NOTIFICATION_BOX, NOTIFICATION_TITLE, NOTIFICATION_DESCRIPTION
from src.models.order import Order

def validate_notification(driver, order: Order):
    """Validate order details with notification."""
    try:
        # Wait for the notification pop-up to appear
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