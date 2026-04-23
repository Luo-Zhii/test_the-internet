import unittest
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

logger = logging.getLogger(__name__)

URL = "https://the-internet.herokuapp.com/slow"


class TestSlowResources(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        logger.info("[TEARDOWN] Quitting driver.")
        self.driver.quit()

    # ─────────────────────────────────────────────────────────────────
    # TC1 – Happy Path: Page eventually loads fully within 30s
    # ─────────────────────────────────────────────────────────────────
    def test_slow_resources_full_load_tc1(self):
        logger.info("[INPUT]  TC1 – Navigating to Slow Resources page (slow loading expected).")
        self.driver.get(URL)

        logger.info("[INPUT]  Using generous 30s wait for the page heading to appear.")
        long_wait = WebDriverWait(self.driver, 30)
        heading = long_wait.until(
            EC.visibility_of_element_located((By.TAG_NAME, "h3"))
        )

        text = heading.text
        logger.info(f"[OUTPUT] Page heading text: '{text}'.")
        self.assertTrue(heading.is_displayed(), "Page heading should be visible once page fully loads.")
        self.assertTrue(len(text) > 0, "Page heading should not be empty.")
        logger.info("[OUTPUT] TC1 PASSED – Slow resources page fully loaded within 30s.")

    # ─────────────────────────────────────────────────────────────────
    # TC2 – Boundary: Verify slow resource appears in Performance API entries
    # ─────────────────────────────────────────────────────────────────
    def test_slow_resources_perf_entry_exists_tc2(self):
        logger.info("[INPUT]  TC2 – Navigating to Slow Resources page.")
        self.driver.get(URL)

        logger.info("[INPUT]  Waiting for page to fully load via heading.")
        long_wait = WebDriverWait(self.driver, 30)
        long_wait.until(EC.visibility_of_element_located((By.TAG_NAME, "h3")))

        logger.info("[INPUT]  Querying Performance API for resource entries related to slow endpoint.")
        entries = self.driver.execute_script(
            "return window.performance.getEntriesByType('navigation');"
        )
        logger.info(f"[OUTPUT] Performance navigation entries count: {len(entries)}.")
        self.assertGreater(
            len(entries), 0,
            "Should have at least one navigation performance entry for the /slow page."
        )

        nav_entry = entries[0]
        duration = nav_entry.get("duration", 0)
        logger.info(f"[OUTPUT] Navigation duration from Performance API: {duration}ms.")
        self.assertGreater(
            duration, 0,
            "Navigation duration must be > 0ms — indicates real network round-trip occurred."
        )
        logger.info("[OUTPUT] TC2 PASSED – Performance API confirms slow resource navigation entry exists.")

    # ─────────────────────────────────────────────────────────────────
    # TC3 – Structure: Verify URL and heading text on Slow Resources page
    # ─────────────────────────────────────────────────────────────────
    def test_slow_resources_page_structure_tc3(self):
        logger.info("[INPUT]  TC3 – Navigating to Slow Resources page.")
        self.driver.get(URL)

        logger.info("[INPUT]  Waiting for heading with 30s generous timeout.")
        long_wait = WebDriverWait(self.driver, 30)
        heading = long_wait.until(EC.visibility_of_element_located((By.TAG_NAME, "h3")))

        current_url = self.driver.current_url
        heading_text = heading.text
        logger.info(f"[OUTPUT] Current URL: '{current_url}'.")
        logger.info(f"[OUTPUT] Heading text: '{heading_text}'.")

        logger.info("[OUTPUT] Asserting URL contains '/slow' endpoint identifier.")
        self.assertIn(
            "/slow", current_url,
            f"URL should contain '/slow' path segment, got: '{current_url}'"
        )
        logger.info("[OUTPUT] Asserting heading is non-empty.")
        self.assertTrue(
            len(heading_text) > 0,
            "Page heading on Slow Resources page should not be empty."
        )
        logger.info("[OUTPUT] TC3 PASSED – Slow Resources page structure verified.")


if __name__ == "__main__":
    unittest.main()
