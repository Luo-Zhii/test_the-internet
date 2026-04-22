import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

class TestEntryAd(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        self.driver.quit()

    def test_entry_ad_modal_close(self):
        # Open the webpage first
        self.driver.get('https://the-internet.herokuapp.com/entry_ad')
        
        # MANDATORY: Delete all cookies to force the ad modal to appear
        self.driver.delete_all_cookies()
        
        # Refresh the page after clearing cookies
        self.driver.refresh()
        
        # Wait for the modal to appear and click the close button
        close_btn = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".modal-footer p")))
        close_btn.click()
        
        # Wait for the modal to completely disappear
        modal = self.driver.find_element(By.ID, "modal")
        self.wait.until(EC.invisibility_of_element(modal))

if __name__ == "__main__":
    unittest.main()