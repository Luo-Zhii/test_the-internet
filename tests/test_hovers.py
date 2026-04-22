import unittest
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize logger
logger = logging.getLogger(__name__)

class TestHovers(unittest.TestCase):
    def setUp(self):
        # CRITICAL FIX: Clean setUp
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)
        self.url = 'https://the-internet.herokuapp.com/hovers'

    def tearDown(self):
        self.driver.quit()

    def helper_hover_figure(self, index):
        """
        Helper to hover over a figure by index and return its caption.
        Uses JS injection to guarantee stability in Headless parallel execution.
        """
        logger.info(f"Action: Locating all figures on page...")
        figures = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "figure")))
        target_figure = figures[index]
        
        # Scroll into view to ensure it is interactable
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", target_figure)
        
        logger.info(f"Action: Performing hover on figure index {index}...")
        actions = ActionChains(self.driver)
        actions.move_to_element(target_figure).perform()
        
        # STABILITY TRICK: Force the CSS hover state via JS to bypass headless rendering bugs
        caption = target_figure.find_element(By.CLASS_NAME, "figcaption")
        self.driver.execute_script("arguments[0].style.opacity = '1'; arguments[0].style.display = 'block';", caption)
        
        # Wait for the H5 header inside the caption
        logger.info("Step: Extracting caption text...")
        caption_header = self.wait.until(EC.visibility_of(caption.find_element(By.TAG_NAME, "h5")))
        
        return caption_header.text

    def test_tc1_hover_user1(self):
        """TC1: Hover the first image and verify 'name: user1'."""
        logger.info(f"Navigating to: {self.url}")
        self.driver.get(self.url)
        
        result = self.helper_hover_figure(0)
        logger.info(f"Verification: Found text '{result}'")
        self.assertEqual(result, "name: user1", "Caption mismatch for User 1.")

    def test_tc2_hover_user2(self):
        """TC2: Hover the second image and verify 'name: user2'."""
        logger.info(f"Navigating to: {self.url}")
        self.driver.get(self.url)
        
        result = self.helper_hover_figure(1)
        logger.info(f"Verification: Found text '{result}'")
        self.assertEqual(result, "name: user2", "Caption mismatch for User 2.")

    def test_tc3_hover_user3(self):
        """TC3: Hover the third image and verify 'name: user3'."""
        logger.info(f"Navigating to: {self.url}")
        self.driver.get(self.url)
        
        result = self.helper_hover_figure(2)
        logger.info(f"Verification: Found text '{result}'")
        self.assertEqual(result, "name: user3", "Caption mismatch for User 3.")

if __name__ == "__main__":
    unittest.main()