from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from src.utils.constants import (NOTIFICATION_BOX, NOTIFICATION_TITLE, NOTIFICATION_DESCRIPTION,
                                 BEARER_TOKEN, ORDER_API_ENDPOINT, PENDING_ORDER_API_ENDPOINT)

def validate_notifications(driver, symbol, order_type, size, units, price, stop_loss, take_profit):
    """Validate order details with API response."""
    try:
        # Wait for the notification pop-up to appear (success or failure)
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, NOTIFICATION_BOX)))
        
        # Get the notification title and description
        notification_title_element = driver.find_elements(By.CSS_SELECTOR, NOTIFICATION_TITLE)
        notification_description_element = driver.find_elements(By.CSS_SELECTOR, NOTIFICATION_DESCRIPTION)

        # Extract text if elements exist
        notification_title = notification_title_element[0].text if notification_title_element else ""
        notification_description = notification_description_element[0].text if notification_description_element else ""
        
        print(f"Notification - Title: {notification_title}. Description: {notification_description}")

        if notification_description != "":
            api_url = PENDING_ORDER_API_ENDPOINT + symbol
            if order_type == "BUY" or order_type == "SELL":
                api_url = ORDER_API_ENDPOINT + symbol

            headers = {
                "Authorization": "Bearer " + BEARER_TOKEN,
                "Content-Type": "application/json"
            }

            # API request
            response = requests.get(api_url, headers=headers)
            
            # Handle 401 error
            if response.status_code == 401:
                print("Error: Unauthorized. Please check your Bearer Token.")
                return
            
            # Handle other non-200 status codes
            if response.status_code != 200:
                print(f"Failed to fetch orders from API. Status code: {response.status_code}")
                return

            # Parse the API response
            orders = response.json().get("result", [])
            if not orders:
                print("No orders found in the API response.")
                return

            # Find the most recent order
            latest_order = orders[0]

            # Extract details from the API response
            api_symbol = latest_order.get("symbol")
            api_units = latest_order.get("units")
            api_size = latest_order.get("lotSize")
            api_open_price = latest_order.get("openPrice")
            api_take_profit = latest_order.get("takeProfit")
            api_stop_loss = latest_order.get("stopLoss")

            api_order_type = latest_order.get("orderType")
            if api_order_type == 0:
                api_order_type = "BUY"
            elif api_order_type == 1:
                api_order_type = "SELL"
            elif api_order_type == 2:
                api_order_type = "BUY LIMIT"
            elif api_order_type == 3:
                api_order_type = "SELL LIMIT"
            elif api_order_type == 4:
                api_order_type = "BUY STOP"
            elif api_order_type == 5:
                api_order_type = "SELL STOP"

            # Compare API values with order details
            if api_symbol != symbol:
                print(f"Wrong symbol: Expected {symbol}, Found {api_symbol}")

            if api_order_type != order_type:
                print(f"Wrong type: Expected {order_type}, Found {api_order_type}")

            if api_units != float(units):
                print(f"Wrong units: Expected {units}, Found {api_units}")

            if api_size != float(size):
                print(f"Wrong size: Expected {size}, Found {api_size}")

            if api_open_price is not None and price is not None:
                if abs(api_open_price - price) > 0.01:
                    print(f"Wrong price: Expected {price:.2f}, Found {api_open_price:.2f}")

            if api_take_profit is not None and take_profit is not None:
                if abs(api_take_profit - take_profit) > 0.01:
                    print(f"Wrong take profit: Expected {take_profit:.2f}, Found {api_take_profit:.2f}")

            if api_stop_loss is not None and stop_loss is not None:
                if abs(api_stop_loss - stop_loss) > 0.01:
                    print(f"Wrong stop loss: Expected {stop_loss:.2f}, Found {api_stop_loss:.2f}")

    except Exception as e:
        print(f"Error validating notifications: {e}")
        raise