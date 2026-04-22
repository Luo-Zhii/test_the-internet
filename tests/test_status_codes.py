import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

class TestStatusCodes(unittest.TestCase):
    def setUp(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        self.driver.quit()

    def test_status_codes_pages(self):
        codes = ["200", "301", "404", "500"]
        
        for code in codes:
            self.driver.get('https://the-internet.herokuapp.com/status_codes')
            
            # Click the code link
            link = self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, code)))
            link.click()
            
            # Verify the status message on the landing page
            status_text = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".example p"))).text
            self.assertIn(f"This page returned a {code} status code.", status_text)
            
            # Go back to the codes list
            self.driver.back()

if __name__ == "__main__":
    unittest.main()
