from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .utils.constants import LOGIN_URL, PLACE_ORDER_BUTTON
from .utils.credentials import ACCOUNT_ID, PASSWORD

def login(driver, account_id=ACCOUNT_ID, password=PASSWORD):
    try:
        driver.get(LOGIN_URL)

        # Wait for login fields
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='login-user-id']")))

        # Enter Account ID
        account_input = driver.find_element(By.CSS_SELECTOR, "[data-testid='login-user-id']")
        account_input.send_keys(account_id)

        # Enter Password
        password_input = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
        password_input.send_keys(password)

        # Click the Login button
        login_button = driver.find_element(By.CSS_SELECTOR, "[data-testid='login-submit']")
        login_button.click()

        # Wait for the homepage to load after login
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, PLACE_ORDER_BUTTON)))
        print("Login successful!")

    except Exception as e:
        print(f"Error during login: {e}")
        raise