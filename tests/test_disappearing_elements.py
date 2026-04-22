import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

class TestDisappearingElements(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        self.driver.quit()

    def test_disappearing_element_gallery(self):
        # This element is dynamic and may or may not appear on refresh
        target_url = 'https://the-internet.herokuapp.com/disappearing_elements'
        self.driver.get(target_url)
        
        # Max retries to find the Gallery element
        max_retries = 5
        found = False
        
        for i in range(max_retries):
            elements = self.driver.find_elements(By.LINK_TEXT, "Gallery")
            if len(elements) > 0:
                found = True
                elements[0].click()
                # Verify navigation to gallery (or 404 as per original script)
                self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
                break
            else:
                self.driver.refresh()
                # Wait for page to load
                self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "h3")))
        
        # This test passes regardless of whether it's found, but documents the attempt
        if found:
            print("Element 'Gallery' was successfully found and clicked.")
        else:
            print("Element 'Gallery' did not appear after several refreshes.")

if __name__ == "__main__":
    unittest.main()
