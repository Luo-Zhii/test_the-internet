import unittest
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

logger = logging.getLogger(__name__)

class TestSecureFileDownload(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)
        self.base_host = "the-internet.herokuapp.com/download_secure"

    def tearDown(self):
        self.driver.quit()

    def test_secure_download_auth_happy_path_tc1(self):
        # Embed credentials via URL injection (Basic Auth bypass)
        auth_url = f"https://admin:admin@{self.base_host}"
        logger.info(f"[INPUT] Navigating with auth: {auth_url}")
        self.driver.get(auth_url)
        
        logger.info("[INPUT] Waiting for secure file links to appear.")
        first_link = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".example a"))
        )
        logger.info(f"[OUTPUT] TC1 Passed: Successfully authenticated. Found file: {first_link.text}")
        self.assertTrue(first_link.is_displayed())

    def test_secure_download_unauth_sad_path_tc2(self):
        unauth_url = f"https://{self.base_host}"
        logger.info(f"[INPUT] Navigating WITHOUT auth: {unauth_url}")
        self.driver.get(unauth_url)
        
        logger.info("[INPUT] Expecting timeout/denial when searching for file links.")
        short_wait = WebDriverWait(self.driver, 3)
        try:
            short_wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".example a")))
            self.fail("Security Bypass: Accessed secure files without credentials!")
        except TimeoutException:
            logger.info("[OUTPUT] TC2 Passed: Access denied as expected (Timeout caught).")

if __name__ == "__main__":
    unittest.main()