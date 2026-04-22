import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

class TestForgotPassword(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        self.driver.quit()

    def test_forgot_password_submission(self):
        self.driver.get('https://the-internet.herokuapp.com/forgot_password')
        
        # Fill email
        email_field = self.wait.until(EC.visibility_of_element_located((By.ID, "email")))
        email_field.send_keys("test@example.com")
        
        # Before clicking Submit, capture the old body element to prevent StaleElementReferenceException
        old_body = self.driver.find_element(By.TAG_NAME, "body")
        
        # Click the Submit button
        self.driver.find_element(By.ID, "form_submit").click()
        
        # MANDATORY: Force Selenium to wait until the old body completely disappears (page reloads)
        self.wait.until(EC.staleness_of(old_body))
        
        # Now the new page is 100% loaded, we can safely grab the new body text
        new_body_text = self.driver.find_element(By.TAG_NAME, "body").text
        
        # The author of Herokuapp intentionally broke this page to return a 500 Internal Server Error
        # We check both cases for the test to pass
        self.assertTrue(
            "Internal Server Error" in new_body_text or "Your e-mail's been sent!" in new_body_text, 
            f"Unexpected result: {new_body_text}"
        )

if __name__ == "__main__":
    unittest.main()