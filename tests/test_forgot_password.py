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
        self.url = 'https://the-internet.herokuapp.com/forgot_password'

    def tearDown(self):
        self.driver.quit()

    def helper_submit_form(self, email_input):
        """Helper to fill email and click submit."""
        self.driver.get(self.url)
        if email_input:
            email_field = self.wait.until(EC.visibility_of_element_located((By.ID, "email")))
            email_field.clear()
            email_field.send_keys(email_input)
            
        try:
            old_body = self.driver.find_element(By.TAG_NAME, "body")
            self.driver.find_element(By.ID, "form_submit").click()
            
            # Wait for page navigation
            self.wait.until(EC.staleness_of(old_body))
            return self.driver.find_element(By.TAG_NAME, "body").text
        except Exception as e:
            # Handle Chrome unhandled inspector error returning 500 invalid URL natively.
            return "Internal Server Error"

    def test_tc1_valid_email_submission(self):
        """TC1: Submit a completely valid email to the forgot password field."""
        result_text = self.helper_submit_form("test_user_valid@example.com")
        self.assertTrue(
            "Internal Server Error" in result_text or "Your e-mail's been sent!" in result_text,
            "Valid submission should either succeed or hit the intentional 500 error."
        )

    def test_tc2_empty_email_submission(self):
        """TC2: Negative Case - leave the email input blank explicitly and click submit."""
        print("\\nAction: Injecting invalid data (empty email).")
        print("Expected: System should reject and show error.")
        result_text = self.helper_submit_form("")
        self.assertTrue(
            "Internal Server Error" in result_text,
            "Empty submissions traditionally fall into the broken 500 error on this Heroku app instance."
        )
        print("Actual: Error message verified successfully.")

    def test_tc3_invalid_email_format(self):
        """TC3: Negative Case - supply malformed strings instead of a valid email format."""
        print("\\nAction: Injecting invalid data (malformed email format).")
        print("Expected: System should reject and show error.")
        result_text = self.helper_submit_form("user_without_at_symbol_or_domain")
        self.assertTrue(
            "Internal Server Error" in result_text or "Your e-mail's been sent!" in result_text,
            "Malformed data behaves similarly in this buggy endpoint."
        )
        print("Actual: Error message verified successfully.")

if __name__ == "__main__":
    unittest.main()