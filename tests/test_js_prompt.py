import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

class TestJSPrompt(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        self.driver.quit()

    def test_js_prompt_text_entry(self):
        self.driver.get('https://the-internet.herokuapp.com/javascript_alerts')
        
        # Locate and click the prompt button
        prompt_btn = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[onclick='jsPrompt()']")))
        prompt_btn.click()
        
        # Switch to alert, send keys, and accept
        self.wait.until(EC.alert_is_present())
        alert = self.driver.switch_to.alert
        test_input = "Antigravity Selenium Test"
        alert.send_keys(test_input)
        alert.accept()
        
        # Verify result message
        result = self.wait.until(EC.visibility_of_element_located((By.ID, "result")))
        self.assertEqual(result.text, f"You entered: {test_input}")

if __name__ == "__main__":
    unittest.main()
