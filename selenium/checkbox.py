from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://the-internet.herokuapp.com/checkboxes")

checkboxes = driver.find_elements(By.CSS_SELECTOR, "#checkboxes input")

for i, checkbox in enumerate(checkboxes, 1):
    if i == 1: 
        if not checkbox.is_selected():
            checkbox.click()
        assert checkbox.is_selected(), f"Checkbox {i} should be checked"
    else:      
        if checkbox.is_selected():
            checkbox.click()
        assert not checkbox.is_selected(), f"Checkbox {i} should be unchecked"

time.sleep(20)

driver.quit()