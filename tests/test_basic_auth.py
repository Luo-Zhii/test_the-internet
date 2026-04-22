import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

class TestBasicAuth(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        self.driver.quit()

    def test_basic_auth_success(self):
        # Passing credentials in the URL
        self.driver.get('https://admin:admin@the-internet.herokuapp.com/basic_auth')
        
        # Verify successful login message
        success_msg_locator = (By.CSS_SELECTOR, ".example p")
        success_msg = self.wait.until(EC.visibility_of_element_located(success_msg_locator))
        
        expected_text = "Congratulations! You must have the proper credentials."
        self.assertIn(expected_text, success_msg.text)

if __name__ == "__main__":
    unittest.main()
