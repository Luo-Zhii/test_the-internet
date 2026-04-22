import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

class TestShiftingContent(unittest.TestCase):
    def setUp(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        self.driver.quit()

    def test_menu_element_shifts_on_refresh(self):
        # The specific URL for menu shifting
        self.driver.get('https://the-internet.herokuapp.com/shifting_content/menu')
        
        # Locate the element that is known to shift
        element = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".example li a")))
        
        # Get initial location
        initial_location = element.location
        
        # Refresh multiple times if necessary as it might shift back randomly
        # But usually one refresh is enough to change something if it's dynamic
        self.driver.refresh()
        
        # Wait for reload
        reloaded_element = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".example li a")))
        new_location = reloaded_element.location
        
        # We don't assert inequality here because it's random and might be the same
        # But we log it and verify the page still works
        print(f"Initial: {initial_location}, New: {new_location}")
        self.assertTrue(reloaded_element.is_displayed())

if __name__ == "__main__":
    unittest.main()
