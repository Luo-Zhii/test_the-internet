import unittest
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, NoSuchFrameException

# Initialize Logger
logger = logging.getLogger(__name__)

class TestFrames(unittest.TestCase):
    def setUp(self):
        logger.info("Initializing webdriver for Frames module.")
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)
        self.base_url = "https://the-internet.herokuapp.com"

    def tearDown(self):
        logger.info("Cleanup: Quitting driver.")
        self.driver.quit()

    # ─────────────────────────────────────────────────────────────────
    # HAPPY PATHS
    # ─────────────────────────────────────────────────────────────────

    def test_iframe_happy_path_tc1(self):
        """TC1: Successfully switch to iFrame and verify input."""
        self.driver.get(f"{self.base_url}/iframe")
        logger.info("[INPUT] Switching to iFrame: mce_0_ifr")
        self.wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, "mce_0_ifr")))
        
        editor = self.driver.find_element(By.ID, "tinymce")
        payload = "Happy Path Test"
        self.driver.execute_script("arguments[0].innerText = arguments[1];", editor, payload)
        
        logger.info(f"[OUTPUT] Verifying content: {editor.text}")
        self.assertEqual(editor.text, payload)
        self.driver.switch_to.default_content()

    def test_nested_frames_happy_path_tc2(self):
        """TC2: Traverse through all nested frames (Full Traversal)."""
        self.driver.get(f"{self.base_url}/nested_frames")
        
        # Top -> Middle (Example of deep dive)
        logger.info("[INPUT] Navigating: Root -> frame-top -> frame-middle")
        self.driver.switch_to.frame("frame-top")
        self.driver.switch_to.frame("frame-middle")
        
        content = self.driver.find_element(By.ID, "content").text
        logger.info(f"[OUTPUT] Middle Frame Content: {content}")
        self.assertEqual(content.strip(), "MIDDLE")
        
        self.driver.switch_to.default_content()

    # ─────────────────────────────────────────────────────────────────
    # SAD PATHS (THE ROBUSTNESS CHECK)
    # ─────────────────────────────────────────────────────────────────

    def test_frame_context_leak_sad_path_tc3(self):
        """TC3: Attempt to find main page elements while trapped in an iFrame."""
        self.driver.get(f"{self.base_url}/iframe")
        self.wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, "mce_0_ifr")))
        
        logger.info("[INPUT] Attempting to find main page <h3> while inside iFrame.")
        try:
            # Heading 'An iFrame containing...' is outside in the main document
            self.driver.find_element(By.TAG_NAME, "h3")
            self.fail("Context Leak: Driver should not see main page elements from inside an iFrame!")
        except NoSuchElementException:
            logger.info("[OUTPUT] Success: NoSuchElementException caught. Context is correctly isolated.")

    def test_invalid_frame_access_sad_path_tc4(self):
        """TC4: Attempt to switch to a non-existent frame ID."""
        self.driver.get(f"{self.base_url}/iframe")
        invalid_id = "ghost_frame_99"
        
        logger.info(f"[INPUT] Attempting to switch to invalid frame: {invalid_id}")
        try:
            self.driver.switch_to.frame(invalid_id)
            self.fail("Error: Switched to a non-existent frame!")
        except NoSuchFrameException:
            logger.info("[OUTPUT] Success: NoSuchFrameException caught as expected.")

    def test_sibling_frame_isolation_sad_path_tc5(self):
        """TC5: From frame-left, attempt to jump directly to frame-right (sibling)."""
        self.driver.get(f"{self.base_url}/nested_frames")
        
        logger.info("[INPUT] Switching to frame-left.")
        self.driver.switch_to.frame("frame-top")
        self.driver.switch_to.frame("frame-left")
        
        logger.info("[INPUT] Attempting direct jump to sibling 'frame-right' without parent switch.")
        try:
            self.driver.switch_to.frame("frame-right")
            self.fail("Error: Direct sibling frame switch should not be possible!")
        except NoSuchFrameException:
            logger.info("[OUTPUT] Success: Switch denied. Driver must return to parent/root context first.")

if __name__ == "__main__":
    unittest.main()