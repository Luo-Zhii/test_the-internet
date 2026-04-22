import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

class TestJSAlerts(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        self.driver.quit()

    def test_js_alert(self):
        self.driver.get('https://the-internet.herokuapp.com/javascript_alerts')
        
        js_alert_btn = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[onclick='jsAlert()']")))
        js_alert_btn.click()
        
        # Switch to alert and accept
        alert = self.driver.switch_to.alert
        alert.accept()
        
        # Verify result
        result = self.wait.until(EC.visibility_of_element_located((By.ID, "result")))
        expected_result = "You successfully clicked an alert"
        self.assertEqual(result.text, expected_result, f"Actual result: {result.text}, Expected result: {expected_result}")

if __name__ == "__main__":
    unittest.main()
