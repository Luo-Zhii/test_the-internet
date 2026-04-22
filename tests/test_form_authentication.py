import unittest
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize professional logger
logger = logging.getLogger(__name__)

class TestFormAuthentication(unittest.TestCase):
    def setUp(self):
        # CRITICAL FIX: Clean setUp to inherit global options from run_fast.py
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)
        self.url = "https://the-internet.herokuapp.com/login"

    def tearDown(self):
        self.driver.quit()

    def helper_login(self, username, password):
        """Helper method to perform login actions."""
        # Ghi nhận INPUT rõ ràng trước khi thao tác
        logger.debug(f"[INPUT] Injecting Credentials -> Username: '{username}' | Password: '{password}'")
        
        self.driver.get(self.url)
        self.wait.until(EC.presence_of_element_located((By.ID, "username"))).clear()
        self.driver.find_element(By.ID, "username").send_keys(username)
        self.driver.find_element(By.ID, "password").clear()
        self.driver.find_element(By.ID, "password").send_keys(password)
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    def get_flash_msg(self):
        """Helper to get the flash notification text."""
        flash = self.wait.until(EC.visibility_of_element_located((By.ID, "flash")))
        text = flash.text.replace("×", "").strip()
        # Ghi nhận OUTPUT rõ ràng sau khi thao tác
        logger.debug(f"[OUTPUT] System responded with Flash Message: '{text}'")
        return text
    # --- TEST CASES ---

    def test_tc1_login_success(self):
        """TC1: Login with valid credentials should redirect to secure area."""
        logger.info("Action: Attempting valid login...")
        self.helper_login("tomsmith", "SuperSecretPassword!")
        flash_text = self.get_flash_msg()
        self.assertIn("/secure", self.driver.current_url)
        self.assertIn("You logged into a secure area!", flash_text)
        logger.info("TC1 Success: Secure area accessed.")

    def test_tc2_invalid_password(self):
        """TC2: Login with wrong password."""
        logger.info("Action: Injecting invalid data (wrong password).")
        self.helper_login("tomsmith", "wrongpassword")
        self.assertIn("Your password is invalid!", self.get_flash_msg())
        logger.info("Actual: Error message verified successfully.")

    def test_tc3_invalid_username(self):
        """TC3: Login with wrong username."""
        logger.info("Action: Injecting invalid data (wrong username).")
        self.helper_login("wronguser", "SuperSecretPassword!")
        self.assertIn("Your username is invalid!", self.get_flash_msg())

    def test_tc4_empty_credentials(self):
        """TC4: Both username and password are empty."""
        logger.info("Action: Injecting invalid data (empty fields).")
        self.helper_login("", "")
        self.assertIn("Your username is invalid!", self.get_flash_msg())

    def test_tc5_empty_password(self):
        """TC5: Username provided but password empty."""
        logger.info("Action: Injecting invalid data (empty password).")
        self.helper_login("tomsmith", "")
        self.assertIn("Your password is invalid!", self.get_flash_msg())

    def test_tc6_empty_username(self):
        """TC6: Password provided but username empty."""
        logger.info("Action: Injecting invalid data (empty username).")
        self.helper_login("", "SuperSecretPassword!")
        self.assertIn("Your username is invalid!", self.get_flash_msg())

    def test_tc7_logout_functionality(self):
        """TC7: Ensure user can logout after successful login."""
        logger.info("Action: Logging in to test logout flow...")
        self.helper_login("tomsmith", "SuperSecretPassword!")
        
        logout_btn = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.button.secondary")))
        logger.info("Action: Clicking logout button...")
        logout_btn.click()
        
        # RACE CONDITION FIX: Wait for the URL to change back to /login before checking the message
        logger.info("Step: Waiting for redirection to complete...")
        self.wait.until(EC.url_contains("/login"))
        
        self.assertIn("You logged out of the secure area!", self.get_flash_msg())
        self.assertEqual(self.driver.current_url, self.url)
        logger.info("TC7 Success: User successfully logged out.")

    def test_tc8_case_sensitive_username(self):
        """TC8: Verify that username is case sensitive."""
        logger.info("Action: Injecting invalid data (wrong case username).")
        self.helper_login("TomSmith", "SuperSecretPassword!")
        self.assertIn("Your username is invalid!", self.get_flash_msg())

    def test_tc9_case_sensitive_password(self):
        """TC9: Verify that password is case sensitive."""
        logger.info("Action: Injecting invalid data (wrong case password).")
        self.helper_login("tomsmith", "supersecretpassword!")
        self.assertIn("Your password is invalid!", self.get_flash_msg())

    def test_tc10_special_characters(self):
        """TC10: Login with special characters in username."""
        logger.info("Action: Injecting invalid data (special chars in username).")
        self.helper_login("!@#$%^&*", "SuperSecretPassword!")
        self.assertIn("Your username is invalid!", self.get_flash_msg())

if __name__ == "__main__":
    unittest.main()