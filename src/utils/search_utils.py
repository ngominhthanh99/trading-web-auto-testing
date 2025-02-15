from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def search(driver, symbol):
    search_bar = driver.find_element(By.CSS_SELECTOR, "[data-testid='symbol-input-search']")
    search_bar.clear()
    search_bar.send_keys(symbol)
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='symbol-input-search-items']"))).click()