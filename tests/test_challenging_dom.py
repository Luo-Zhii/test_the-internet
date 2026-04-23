import unittest
import logging
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TestChallengingDOM(unittest.TestCase):
    def setUp(self):
        logger.info("Initializing webdriver and variables.")
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)
        logger.info("Navigating to Challenging DOM page.")
        self.driver.get("https://the-internet.herokuapp.com/challenging_dom")

    def tearDown(self):
        logger.info("Quitting driver.")
        self.driver.quit()

    def test_dynamic_buttons_tc1(self):
        logger.info("Executing TC1_Dynamic_Buttons: Locate the Red button without using ID. Click and assert.")
        logger.info("Action: Locating the Red button via CSS Selector '.button.alert'.")
        red_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".button.alert")))
        time.sleep(2)
        logger.info("Action: Clicking the Red button.")
        red_button.click()
        
        logger.info("Expectation: Button click is processed, and it remains visible or dynamic DOM reloads.")
        # Re-locate due to DOM reload after clicking to avoid StaleElementReferenceException
        red_button_after = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".button.alert")))
        self.assertTrue(red_button_after.is_displayed(), "Red button should be displayed")
        logger.info("Assertion passed.")

    def test_table_ep_mid_tc2(self):
        logger.info("Executing TC2_Table_EP_Mid: Extract and verify data from Row 5.")
        logger.info("Action: Locating the fifth row using XPath './/table/tbody/tr[5]'.")
        row_5 = self.wait.until(EC.presence_of_element_located((By.XPATH, "//table/tbody/tr[5]")))
        
        logger.info("Action: Extracting text from Row 5.")
        text = row_5.text
        logger.info(f"Retrieved text: {text}")
        
        logger.info("Expectation: Text from Row 5 should contain expected EP data.")
        self.assertTrue(len(text) > 0, "Row 5 text should not be empty")
        self.assertTrue("Iuvaret4" in text or "Apeirian4" in text, f"Unexpected row 5 content: {text}")
        logger.info("Assertion passed.")

    def test_table_bva_min_tc3(self):
        logger.info("Executing TC3_Table_BVA_Min: Extract and verify data from Row 1.")
        logger.info("Action: Locating the first row using XPath './/table/tbody/tr[1]'.")
        row_1 = self.wait.until(EC.presence_of_element_located((By.XPATH, "//table/tbody/tr[1]")))
        
        logger.info("Action: Extracting text from Row 1.")
        text = row_1.text
        logger.info(f"Retrieved text: {text}")
        
        logger.info("Expectation: Text from Row 1 should contain expected BVA min data.")
        self.assertTrue(len(text) > 0, "Row 1 text should not be empty")
        self.assertTrue("Iuvaret0" in text or "Apeirian0" in text, f"Unexpected row 1 content: {text}")
        logger.info("Assertion passed.")

    def test_table_bva_max_tc4(self):
        logger.info("Executing TC4_Table_BVA_Max: Extract and verify data from Row 10.")
        logger.info("Action: Locating the tenth row using XPath './/table/tbody/tr[10]'.")
        row_10 = self.wait.until(EC.presence_of_element_located((By.XPATH, "//table/tbody/tr[10]")))
        
        logger.info("Action: Extracting text from Row 10.")
        text = row_10.text
        logger.info(f"Retrieved text: {text}")
        
        logger.info("Expectation: Text from Row 10 should contain expected BVA max data.")
        self.assertTrue(len(text) > 0, "Row 10 text should not be empty")
        self.assertTrue("Iuvaret9" in text or "Apeirian9" in text, f"Unexpected row 10 content: {text}")
        logger.info("Assertion passed.")

    def test_table_negative_out_of_bounds_tc5(self):
        logger.info("Executing TC5_Table_Negative_OutOfBounds: Attempt to locate Row 11.")
        logger.info("Action: Switching to a short explicit wait of 2 seconds.")
        short_wait = WebDriverWait(self.driver, 2)
        
        logger.info("Expectation: TimeoutException or NoSuchElementException should be gracefully caught.")
        try:
            short_wait.until(EC.presence_of_element_located((By.XPATH, "//table/tbody/tr[11]")))
            logger.info("Unexpected: Row 11 was found.")
            self.fail("Row 11 should not exist")
        except TimeoutException:
            logger.info("TimeoutException was gracefully caught. Row 11 does not exist.")
        except NoSuchElementException:
            logger.info("NoSuchElementException was gracefully caught. Row 11 does not exist.")
        
        logger.info("Assertion passed.")

    def test_canvas_verification_tc6(self):
        logger.info("Executing TC6_Canvas_Verification: Verify the presence of the Canvas element.")
        logger.info("Action: Locating the canvas element.")
        canvas = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "canvas#canvas")))
        
        logger.info("Expectation: Canvas element should be displayed.")
        self.assertTrue(canvas.is_displayed(), "Canvas element should be present and visible on the page.")
        logger.info("Assertion passed.")

    def test_table_action_links_tc7(self):
        """TC7_Table_Action_Links: Interact with 'edit' and 'delete' links in a specific row."""
        logger.info("Action: Locating the 'edit' link in Row 3.")
        # Using XPath to find the 'edit' link specifically inside the 3rd row
        edit_link = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//table/tbody/tr[3]/td[7]/a[@href='#edit']")))
        
        logger.info("Action: Clicking the 'edit' link.")
        edit_link.click()
        
        logger.info("Verification: Asserting URL contains '#edit'.")
        self.assertIn("#edit", self.driver.current_url, "Clicking 'edit' did not update the URL fragment correctly.")
        
        logger.info("Action: Locating the 'delete' link in Row 3.")
        delete_link = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//table/tbody/tr[3]/td[7]/a[@href='#delete']")))
        
        logger.info("Action: Clicking the 'delete' link.")
        delete_link.click()
        
        logger.info("Verification: Asserting URL contains '#delete'.")
        self.assertIn("#delete", self.driver.current_url, "Clicking 'delete' did not update the URL fragment correctly.")
        logger.info("Assertion passed.")
if __name__ == "__main__":
    unittest.main()
