import unittest
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

# Initialize logger for traceability in the HTML report
logger = logging.getLogger(__name__)

class TestJSAlerts(unittest.TestCase):
    def setUp(self):
        options = webdriver.ChromeOptions()
        # Ensure consistent resolution to prevent "maximize_window" crashes in headless mode
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        
        # REMOVED: self.driver.maximize_window() -> This causes crashes in specific Linux/Headless environments
        self.wait = WebDriverWait(self.driver, 10)
        self.url = 'https://the-internet.herokuapp.com/javascript_alerts'

    def tearDown(self):
        self.driver.quit()

    def get_result_text(self):
        """Helper to safely retrieve the result message from the UI."""
        return self.wait.until(EC.visibility_of_element_located((By.ID, "result"))).text

    def test_tc1_accept_js_alert(self):
        """TC1: Accept a standard JS Alert and verify the underlying success message."""
        logger.info(f"Navigating to: {self.url}")
        self.driver.get(self.url)
        
        logger.info("Action: Triggering JS Alert...")
        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[onclick='jsAlert()']"))).click()
        
        logger.info("Action: Switching to Alert and accepting...")
        self.wait.until(EC.alert_is_present())
        alert = self.driver.switch_to.alert
        self.assertEqual(alert.text, "I am a JS Alert", "Alert text mismatch.")
        alert.accept()
        
        result = self.get_result_text()
        logger.info(f"Verification: Result message is '{result}'")
        self.assertEqual(result, "You successfully clicked an alert")

    def test_tc2_accept_js_confirm(self):
        """TC2: Accept a JS Confirmation dialog."""
        logger.info(f"Navigating to: {self.url}")
        self.driver.get(self.url)
        
        logger.info("Action: Triggering JS Confirm...")
        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[onclick='jsConfirm()']"))).click()
        
        self.wait.until(EC.alert_is_present())
        alert = self.driver.switch_to.alert
        alert.accept()
        
        result = self.get_result_text()
        logger.info(f"Verification: Confirmation result is '{result}'")
        self.assertEqual(result, "You clicked: Ok")

    def test_tc3_dismiss_js_confirm(self):
        """TC3: Negative Case - Dismiss (Cancel) a JS Confirmation dialog."""
        logger.info("Starting TC3: Negative/Dismiss Path")
        self.driver.get(self.url)
        
        logger.info("Action: Triggering JS Confirm to dismiss...")
        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[onclick='jsConfirm()']"))).click()
        
        self.wait.until(EC.alert_is_present())
        alert = self.driver.switch_to.alert
        
        logger.info("Expected: System should handle the cancellation gracefully.")
        alert.dismiss()
        
        result = self.get_result_text()
        logger.info(f"Actual: Result message verified as '{result}'")
        self.assertEqual(result, "You clicked: Cancel")

if __name__ == "__main__":
    unittest.main()