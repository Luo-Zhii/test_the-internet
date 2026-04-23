import unittest
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchFrameException

logger = logging.getLogger(__name__)

class TestNestedFrames(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)
        self.url = "https://the-internet.herokuapp.com/nested_frames"

    def tearDown(self):
        self.driver.quit()

    def test_nested_frames_top_traversal_tc1(self):
        self.driver.get(self.url)
        logger.info("[INPUT] Traversing TOP -> LEFT")
        self.driver.switch_to.frame("frame-top")
        self.driver.switch_to.frame("frame-left")
        self.assertEqual(self.driver.find_element(By.TAG_NAME, "body").text.strip(), "LEFT")

        logger.info("[INPUT] Traversing LEFT -> TOP -> MIDDLE")
        self.driver.switch_to.parent_frame()
        self.driver.switch_to.frame("frame-middle")
        self.assertEqual(self.driver.find_element(By.ID, "content").text.strip(), "MIDDLE")

        logger.info("[INPUT] Traversing MIDDLE -> TOP -> RIGHT")
        self.driver.switch_to.parent_frame()
        self.driver.switch_to.frame("frame-right")
        self.assertEqual(self.driver.find_element(By.TAG_NAME, "body").text.strip(), "RIGHT")
        logger.info("[OUTPUT] TC1 Passed: All Top frames verified.")

    def test_nested_frames_bottom_traversal_tc2(self):
        self.driver.get(self.url)
        logger.info("[INPUT] Traversing ROOT -> BOTTOM")
        self.driver.switch_to.default_content()
        self.driver.switch_to.frame("frame-bottom")
        self.assertEqual(self.driver.find_element(By.TAG_NAME, "body").text.strip(), "BOTTOM")
        logger.info("[OUTPUT] TC2 Passed: Bottom frame verified.")

    def test_nested_frames_sibling_isolation_tc3(self):
        self.driver.get(self.url)
        self.driver.switch_to.frame("frame-top")
        self.driver.switch_to.frame("frame-left")
        
        logger.info("[INPUT] Attempting illegal jump: LEFT directly to RIGHT")
        try:
            self.driver.switch_to.frame("frame-right")
            self.fail("Context Leak: Sibling jump should not be allowed.")
        except NoSuchFrameException:
            logger.info("[OUTPUT] TC3 Passed: Sibling isolation enforced.")

if __name__ == "__main__":
    unittest.main()