import unittest
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

BASE_URL = "https://the-internet.herokuapp.com/abtest"
VALID_HEADERS = ["A/B Test Control", "A/B Test Variation 1"]


class TestABTesting(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        logger.info("[TEARDOWN] Quitting driver.")
        self.driver.quit()

    # ─────────────────────────────────────────────────────────────────
    # TC1 – Happy Path: Header reflects a valid A/B variant
    # ─────────────────────────────────────────────────────────────────
    def test_ab_testing_header_variation_tc1(self):
        logger.info("[INPUT]  TC1 – Navigating to A/B Testing page.")
        self.driver.get(BASE_URL)

        logger.info("[INPUT]  Waiting for the h3 header element to be visible.")
        header = self.wait.until(
            EC.visibility_of_element_located((By.TAG_NAME, "h3"))
        )

        text = header.text
        logger.info(f"[INPUT]  Retrieved header text: '{text}'.")

        logger.info(f"[OUTPUT] Asserting header text is one of the known variants: {VALID_HEADERS}.")
        self.assertIn(
            text,
            VALID_HEADERS,
            f"Header '{text}' is not a recognized A/B variant. Expected one of: {VALID_HEADERS}"
        )
        logger.info("[OUTPUT] TC1 PASSED – Header matches a valid A/B variant.")

    # ─────────────────────────────────────────────────────────────────
    # TC2 – UI Check: Informational paragraph is always present
    # ─────────────────────────────────────────────────────────────────
    def test_ab_testing_paragraph_presence_tc2(self):
        logger.info("[INPUT]  TC2 – Navigating to A/B Testing page.")
        self.driver.get(BASE_URL)

        logger.info("[INPUT]  Waiting for the paragraph containing 'Also known as split testing'.")
        # Locate the paragraph by partial text using XPath
        paragraph = self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//p[contains(text(),'Also known as split testing')]")
            )
        )

        logger.info("[OUTPUT] Asserting the informational paragraph is displayed.")
        self.assertTrue(
            paragraph.is_displayed(),
            "The paragraph 'Also known as split testing' should be visible on the page."
        )
        logger.info("[OUTPUT] TC2 PASSED – Paragraph is present and visible.")

    # ─────────────────────────────────────────────────────────────────
    # TC3 – Robustness: Opt-out cookie does not break the page
    # ─────────────────────────────────────────────────────────────────
    def test_ab_testing_optout_cookie_tc3(self):
        logger.info("[INPUT]  TC3 – Navigating to A/B Testing page before setting cookie.")
        # Must navigate first so the domain is set before adding a cookie
        self.driver.get(BASE_URL)

        logger.info("[INPUT]  Adding A/B opt-out cookie: {'name': 'optimizelyOptOut', 'value': 'true'}.")
        self.driver.add_cookie({'name': 'optimizelyOptOut', 'value': 'true'})

        logger.info("[INPUT]  Refreshing the page with the opt-out cookie active.")
        self.driver.refresh()

        logger.info("[INPUT]  Waiting for the h3 header element to be visible after refresh.")
        header = self.wait.until(
            EC.visibility_of_element_located((By.TAG_NAME, "h3"))
        )

        text = header.text
        logger.info(f"[INPUT]  Retrieved header text post-cookie: '{text}'.")

        logger.info("[OUTPUT] Asserting the page explicitly shows 'No A/B Test' when opted out.")
        # FIX: The expected behavior of the opt-out cookie is to show "No A/B Test"
        self.assertEqual(
            text,
            "No A/B Test",
            f"Expected header to be 'No A/B Test' after opt-out, but got '{text}'."
        )
        logger.info("[OUTPUT] TC3 PASSED – Opt-out cookie successfully bypassed the A/B test variations.")

if __name__ == "__main__":
    unittest.main()
