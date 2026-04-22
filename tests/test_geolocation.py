import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

class TestGeolocation(unittest.TestCase):
    def setUp(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        # Pre-approve geolocation permission for headless/CI compatibility if possible
        # However, for this specific test button, it's usually enough to just click and wait.
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        self.driver.quit()

    def test_geolocation_reveal(self):
        self.driver.get('https://the-internet.herokuapp.com/geolocation')
        
        # Click the "Where am I?" button
        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".example button"))).click()
        
        # Verify coordinates appear
        lat = self.wait.until(EC.visibility_of_element_located((By.ID, "lat-value")))
        long = self.wait.until(EC.visibility_of_element_located((By.ID, "long-value")))
        
        self.assertTrue(lat.text)
        self.assertTrue(long.text)
        
        # Verify Google Maps link appears
        map_link = self.driver.find_element(By.CSS_SELECTOR, "#map-link a")
        self.assertTrue(map_link.is_displayed())

if __name__ == "__main__":
    unittest.main()
