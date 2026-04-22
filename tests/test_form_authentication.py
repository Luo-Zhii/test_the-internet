import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

class TestFormAuthentication(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        self.driver.quit()

    # --- HELPER METHOD: Do not start with 'test_' ---
    def helper_login(self):
        self.driver.get('https://the-internet.herokuapp.com/login')
        
        # Fill credentials and submit
        self.wait.until(EC.visibility_of_element_located((By.ID, "username"))).send_keys("tomsmith")
        self.driver.find_element(By.ID, "password").send_keys("SuperSecretPassword!")
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    # --- TEST CASES ---
    def test_form_login_success(self):
        # Call the helper to perform login actions
        self.helper_login()
        
        # Verify login success message
        flash_msg = self.wait.until(EC.visibility_of_element_located((By.ID, "flash")))
        self.assertIn("You logged into a secure area!", flash_msg.text)

    def test_form_logout(self):
        # Call the helper to login first
        self.helper_login()
        
        # Capture the green login success message before clicking logout
        old_flash = self.driver.find_element(By.ID, "flash")
        
        # Click the logout button
        logout_btn = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.button.secondary.radius")))
        logout_btn.click()
        
        # MANDATORY: Wait for the old login message to completely disappear (Staleness)
        self.wait.until(EC.staleness_of(old_flash))
        
        # Verify logout success message
        new_flash_msg = self.wait.until(EC.visibility_of_element_located((By.ID, "flash")))
        self.assertIn("You logged out of the secure area!", new_flash_msg.text)

if __name__ == "__main__":
    unittest.main()