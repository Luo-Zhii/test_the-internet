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
        
        # 1. Preemptively grant location permissions internally in Chrome
        prefs = {"profile.default_content_setting_values.geolocation": 1}
        options.add_experimental_option("prefs", prefs)
        
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        
        # 2. THE SENIOR TRICK: Mocking Geolocation via Chrome DevTools Protocol (CDP)
        # This prevents OS-level popups and guarantees consistent test data.
        # Coordinates set to Hanoi, Vietnam.
        mock_location_params = {
            "latitude": 21.0285,
            "longitude": 105.8542,
            "accuracy": 100
        }
        self.driver.execute_cdp_cmd("Emulation.setGeolocationOverride", mock_location_params)
        
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)
        self.url = 'https://the-internet.herokuapp.com/geolocation'

    def tearDown(self):
        self.driver.quit()

    def test_tc1_geolocation_reveal_coordinates(self):
        """TC1: Clicking 'Where am I?' populates the latitude and longitude fields."""
        print("\nStep 1: Navigating to Geolocation page...")
        self.driver.get(self.url)
        
        print("Step 2: Clicking the 'Where am I?' button...")
        btn = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".example button")))
        btn.click()
        
        print("Step 3: Waiting for coordinates to be rendered...")
        lat = self.wait.until(EC.visibility_of_element_located((By.ID, "lat-value")))
        long = self.wait.until(EC.visibility_of_element_located((By.ID, "long-value")))
        
        print(f"Expected: Valid float numbers. Actual: Lat = {lat.text}, Long = {long.text}")
        
        try:
            float(lat.text)
            float(long.text)
            self.assertTrue(True)
        except ValueError:
            self.fail("Latitude and Longitude were not valid numbers.")

    def test_tc2_geolocation_map_link(self):
        """TC2: Ensure the Google Maps link appears and has a valid dynamic href."""
        print("\nStep 1: Navigating to Geolocation page...")
        self.driver.get(self.url)
        
        print("Step 2: Clicking the 'Where am I?' button...")
        btn = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".example button")))
        btn.click()
        
        print("Step 3: Extracting Map URL...")
        map_link = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#map-link a")))
        href = map_link.get_attribute("href")
        
        print(f"Generated Map URL: {href}")
        
        # Assertion 1: Check if it's a Google Maps link
        self.assertIn("google", href, "Map link must contain Google maps URL structure.")
        
        # Assertion 2: Verify the dynamically generated lat value is injected into the URL
        lat = self.driver.find_element(By.ID, "lat-value").text
        self.assertIn(lat, href, "The generated URL must contain the correct latitude.")

if __name__ == "__main__":
    unittest.main()