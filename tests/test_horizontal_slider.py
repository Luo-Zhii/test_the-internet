import unittest
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

logger = logging.getLogger(__name__)

class TestHorizontalSlider(unittest.TestCase):
    def setUp(self):
        options = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.wait = WebDriverWait(self.driver, 10)
        self.url = "https://the-internet.herokuapp.com/horizontal_slider"

    def tearDown(self):
        self.driver.quit()

    def test_tc1_slider_increments_correctly(self):
        """TC1: Verify slider increments by 0.5 relative to its current position."""
        logger.info("Step 1: Navigating to Horizontal Slider...")
        self.driver.get(self.url)
        
        slider = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='range']")))
        range_val = self.driver.find_element(By.ID, "range")
        
        # Read initial value instead of assuming it's 0
        initial_value = float(range_val.text)
        logger.info(f"Initial slider value is: {initial_value}")
        
        logger.info("Step 2: Pressing ARROW_RIGHT...")
        slider.send_keys(Keys.ARROW_RIGHT)
        
        new_value = float(range_val.text)
        expected_value = initial_value + 0.5
        
        logger.info(f"Expected: {expected_value}, Actual: {new_value}")
        self.assertEqual(new_value, expected_value, "Slider did not increment by exactly 0.5.")

    def test_tc2_slider_boundary_min(self):
        """TC2: Verify slider cannot go below 0."""
        logger.info("Step 1: Navigating to Horizontal Slider...")
        self.driver.get(self.url)
        
        slider = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='range']")))
        
        logger.info("Step 2: Spamming ARROW_LEFT 15 times to hit the floor boundary...")
        for _ in range(15):
            slider.send_keys(Keys.ARROW_LEFT)
            
        final_value = self.driver.find_element(By.ID, "range").text
        logger.info(f"Final value hit: {final_value}")
        
        self.assertEqual(final_value, "0", "Slider failed to hit the hard minimum boundary of 0.")

if __name__ == "__main__":
    unittest.main()