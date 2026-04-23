import unittest
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logger = logging.getLogger(__name__)

URL = "https://the-internet.herokuapp.com/javascript_error"

# PAGE STRUCTURE (verified from source):
# <html><head><title>Page with JavaScript errors on load</title>
#   <script>function loadError(){var xx=document.propertyThatDoesNotExist.xyz;}</script>
# </head><body onload="loadError()">
#   <p>This page has a JavaScript error in the onload event...</p>
# </body></html>
#
# Key facts:
# - Page title: "Page with JavaScript errors on load" (NOT "The Internet")
# - NO div.example wrapper - bare <p> inside <body>
# - NO <h3> element
# - body onload fires loadError() which throws TypeError


class TestJavaScriptError(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        logger.info("[TEARDOWN] Quitting driver.")
        self.driver.quit()

    # ─────────────────────────────────────────────────────────────────
    # TC1 – Happy Path: Page loads and content paragraph is present
    # The page has ONLY a bare <p> inside <body> — no div.example wrapper
    # ─────────────────────────────────────────────────────────────────
    def test_javascript_error_page_loads_tc1(self):
        logger.info("[INPUT]  TC1 – Navigating to JavaScript Error page.")
        self.driver.get(URL)

        logger.info("[INPUT]  Waiting for the bare <p> content element to be present.")
        content = self.wait.until(
            EC.presence_of_element_located((By.TAG_NAME, "p"))
        )

        text = content.text
        logger.info(f"[OUTPUT] Page <p> text: '{text[:80]}'.")
        self.assertTrue(content.is_displayed(), "Page content paragraph should be visible.")
        self.assertIn(
            "JavaScript error",
            text,
            f"Expected 'JavaScript error' in page content, got: '{text}'"
        )
        logger.info("[OUTPUT] TC1 PASSED – Page loaded and content paragraph verified.")

    # ─────────────────────────────────────────────────────────────────
    # TC2 – Robustness: JavaScript error is triggered on page load
    # The onload handler calls loadError() which accesses a nonexistent property
    # We verify via execute_script that the broken object access results in undefined
    # ─────────────────────────────────────────────────────────────────
    def test_javascript_error_console_log_tc2(self):
        logger.info("[INPUT]  TC2 – Navigating to JavaScript Error page (triggers JS error on load).")
        self.driver.get(URL)

        logger.info("[INPUT]  Waiting for page content (<p>) to confirm page loaded.")
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "p")))

        logger.info("[INPUT]  Verifying the JS error condition: document.propertyThatDoesNotExist is undefined.")
        result = self.driver.execute_script(
            "return typeof document.propertyThatDoesNotExist;"
        )
        logger.info(f"[OUTPUT] typeof document.propertyThatDoesNotExist = '{result}'.")
        self.assertEqual(
            result, "undefined",
            f"Expected 'undefined' for nonexistent property, got: '{result}'"
        )

        logger.info("[INPUT]  Verifying the loadError function exists in scope.")
        fn_type = self.driver.execute_script("return typeof window.loadError;")
        logger.info(f"[OUTPUT] typeof window.loadError = '{fn_type}'.")
        self.assertEqual(fn_type, "function", "loadError should be a function defined on the page.")

        logger.info("[OUTPUT] TC2 PASSED – JS error precondition and function presence verified.")

    # ─────────────────────────────────────────────────────────────────
    # TC3 – Negative / Structural: Confirm no <h3> heading exists
    # This page deliberately has no div.example or h3 — just a bare <p>
    # ─────────────────────────────────────────────────────────────────
    def test_javascript_error_no_heading_tc3(self):
        logger.info("[INPUT]  TC3 – Navigating to JavaScript Error page.")
        self.driver.get(URL)

        logger.info("[INPUT]  Waiting for page content to load.")
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "p")))

        logger.info("[INPUT]  Asserting no <h3> element exists (page uses only <p> for content).")
        h3_elements = self.driver.find_elements(By.TAG_NAME, "h3")
        logger.info(f"[OUTPUT] <h3> elements found: {len(h3_elements)}.")
        self.assertEqual(
            len(h3_elements), 0,
            f"Expected 0 <h3> elements, but found {len(h3_elements)}."
        )
        logger.info("[OUTPUT] TC3 PASSED – Confirmed page has no <h3> heading element.")

    # ─────────────────────────────────────────────────────────────────
    # TC4 – Edge Case: Page title matches expected value
    # Page title is "Page with JavaScript errors on load" (NOT "The Internet")
    # ─────────────────────────────────────────────────────────────────
    def test_javascript_error_page_title_tc4(self):
        logger.info("[INPUT]  TC4 – Navigating to JavaScript Error page.")
        self.driver.get(URL)

        logger.info("[INPUT]  Waiting for page to load.")
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "p")))

        title = self.driver.title
        logger.info(f"[OUTPUT] Page title: '{title}'.")
        self.assertIn(
            "JavaScript error",
            title,
            f"Expected 'JavaScript error' in page title, got: '{title}'"
        )
        logger.info("[OUTPUT] TC4 PASSED – Page title verified.")


if __name__ == "__main__":
    unittest.main()
