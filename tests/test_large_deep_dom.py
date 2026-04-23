import unittest
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

logger = logging.getLogger(__name__)

URL = "https://the-internet.herokuapp.com/large"

# REAL page structure (verified from source):
# - div id='no-siblings'         → the simple "No Siblings" section
# - div id='sibling-N.M'        → siblings section, e.g. sibling-2.2 has text "2.2"
# - id='header-N'               → table section headers (header-1 through header-50)
# The page DOES have an h3 ("Large & Deep DOM") and h4 headings
# NO "large-N-N" style IDs exist on this page.


class TestLargeDeepDOM(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        logger.info("[TEARDOWN] Quitting driver.")
        self.driver.quit()

    # ─────────────────────────────────────────────────────────────────
    # TC1 – Happy Path: Verify exact text of a deep sibling element
    # Real IDs: sibling-N.M (e.g. sibling-2.2 contains text "2.2")
    # ─────────────────────────────────────────────────────────────────
    def test_large_dom_deep_sibling_tc1(self):
        logger.info("[INPUT]  TC1 – Navigating to Large & Deep DOM page.")
        self.driver.get(URL)

        logger.info("[INPUT]  Waiting for page heading (h3) to confirm page loaded.")
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "h3")))

        # Real sibling element IDs use format: sibling-N.M
        target_id = "sibling-2.2"
        logger.info(f"[INPUT]  Locating deep sibling element by ID: #{target_id}.")
        element = self.wait.until(EC.presence_of_element_located((By.ID, target_id)))

        text = element.text
        logger.info(f"[OUTPUT] Element #{target_id} text: '{text}'.")
        self.assertTrue(len(text) > 0, f"Element #{target_id} should have non-empty text.")
        self.assertIn("2.2", text, f"Expected '2.2' in element text but got: '{text}'")
        logger.info("[OUTPUT] TC1 PASSED – Deep sibling element located and text verified.")

    # ─────────────────────────────────────────────────────────────────
    # TC2 – Happy Path: Verify all sibling-N.M elements are present via JS
    # Dynamically discovers all elements with ID prefix 'sibling-'
    # ─────────────────────────────────────────────────────────────────
    def test_large_dom_boundary_cell_tc2(self):
        logger.info("[INPUT]  TC2 – Navigating to Large & Deep DOM page.")
        self.driver.get(URL)

        logger.info("[INPUT]  Waiting for page heading (h3) to be present.")
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "h3")))

        logger.info("[INPUT]  Using JS to discover all element IDs matching 'sibling-N.N' pattern.")
        all_sibling_ids = self.driver.execute_script(
            "return Array.from(document.querySelectorAll('[id^=\"sibling-\"]'))"
            ".map(e => e.id).filter(id => /^sibling-\\d+\\.\\d+$/.test(id));"
        )
        logger.info(f"[OUTPUT] Found {len(all_sibling_ids)} sibling-* elements. Sample: {all_sibling_ids[:5]}.")
        self.assertGreater(len(all_sibling_ids), 0, "Should find at least one sibling-N.M element on the page.")

        # Sort numerically to find the BVA-max (e.g. sibling-50.3)
        def sort_key(eid):
            parts = eid.replace("sibling-", "").split(".")
            return (int(parts[0]), int(parts[1]))

        sorted_ids = sorted(all_sibling_ids, key=sort_key)
        boundary_id = sorted_ids[-1]
        logger.info(f"[INPUT]  True BVA-max boundary ID discovered: #{boundary_id}.")

        element = self.driver.find_element(By.ID, boundary_id)
        text = element.text
        logger.info(f"[OUTPUT] Boundary cell #{boundary_id} text: '{text}'.")

        logger.info("[OUTPUT] Asserting boundary cell is present and has non-empty text.")
        self.assertIsNotNone(element, f"Boundary cell #{boundary_id} should exist in the DOM.")
        self.assertTrue(len(text) > 0, f"Boundary cell #{boundary_id} should have non-empty text.")
        logger.info(f"[OUTPUT] TC2 PASSED – True BVA-max boundary verified at #{boundary_id}.")

    # ─────────────────────────────────────────────────────────────────
    # TC3 – Sad Path: Invalid element ID → TimeoutException
    # ─────────────────────────────────────────────────────────────────
    def test_large_dom_invalid_id_sad_path_tc3(self):
        logger.info("[INPUT]  TC3 – Navigating to Large & Deep DOM page.")
        self.driver.get(URL)

        logger.info("[INPUT]  Waiting for page heading to confirm load.")
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "h3")))

        invalid_id = "large-999-999"
        logger.info(f"[INPUT]  Attempting to locate non-existent element: #{invalid_id} (2s short-wait).")
        short_wait = WebDriverWait(self.driver, 2)
        try:
            short_wait.until(EC.presence_of_element_located((By.ID, invalid_id)))
            self.fail(f"Element #{invalid_id} should NOT exist in the DOM.")
        except TimeoutException:
            logger.info("[OUTPUT] TimeoutException caught – invalid element ID correctly absent.")

        logger.info("[OUTPUT] TC3 PASSED – Non-existent deep ID gracefully handled.")

    # ─────────────────────────────────────────────────────────────────
    # TC4 – Sad Path: Invalid XPath → TimeoutException
    # ─────────────────────────────────────────────────────────────────
    def test_large_dom_invalid_xpath_sad_path_tc4(self):
        logger.info("[INPUT]  TC4 – Navigating to Large & Deep DOM page.")
        self.driver.get(URL)

        logger.info("[INPUT]  Waiting for page heading to confirm load.")
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "h3")))

        # A plausible-but-invalid XPath — no such element will be found
        invalid_xpath = "//div[@id='sibling-999.999']"
        logger.info(f"[INPUT]  Attempting to find element via invalid XPath: '{invalid_xpath}' (2s short-wait).")
        short_wait = WebDriverWait(self.driver, 2)
        try:
            short_wait.until(EC.presence_of_element_located((By.XPATH, invalid_xpath)))
            self.fail("Element via invalid XPath should NOT be found.")
        except TimeoutException:
            logger.info("[OUTPUT] TimeoutException caught – invalid XPath target correctly absent.")

        logger.info("[OUTPUT] TC4 PASSED – Invalid deep XPath gracefully handled.")


if __name__ == "__main__":
    unittest.main()
