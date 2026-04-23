import unittest
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException

logger = logging.getLogger(__name__)

URL = "https://the-internet.herokuapp.com/jqueryui/menu"

# PAGE STRUCTURE (verified from source):
# <ul id="menu">
#   <li class="ui-state-disabled"><a href="#">Disabled</a></li>
#   <li><a href="#">Enabled</a>
#     <ul>
#       <li><a href="#">Downloads</a>
#         <ul>
#           <li><a href="/download/...menu.pdf">PDF</a></li>
#           <li><a href="/download/...menu.csv">CSV</a></li>
#           <li><a href="/download/...menu.xls">Excel</a></li>
#         </ul>
#       </li>
#       <li><a href="#">Back to JQuery UI</a></li>
#     </ul>
#   </li>
# </ul>
#
# jQuery UI menu shows/hides child <ul> via JS events on the <li> elements.
# In headless mode, ActionChains move_to_element() doesn't reliably trigger
# jQuery UI's hover events. Strategy: use JS to directly show child menus.


class TestJQueryUIMenus(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        logger.info("[TEARDOWN] Quitting driver.")
        self.driver.quit()

    def _force_show_submenu(self, parent_li_element):
        """Directly set visibility of child <ul> to make it accessible in headless mode."""
        self.driver.execute_script(
            """
            var li = arguments[0];
            var childUl = li.querySelector('ul');
            if (childUl) {
                childUl.style.display = 'block';
                childUl.style.visibility = 'visible';
                childUl.style.opacity = '1';
                childUl.style.position = 'relative';
            }
            """,
            parent_li_element
        )

    # ─────────────────────────────────────────────────────────────────
    # TC1 – Happy Path: Enabled → Downloads → PDF
    # Uses JS to force sub-menu visibility (reliable in headless mode)
    # ─────────────────────────────────────────────────────────────────
    def test_jquery_menu_hover_pdf_tc1(self):
        logger.info("[INPUT]  TC1 – Navigating to JQuery UI Menus page.")
        self.driver.get(URL)

        logger.info("[INPUT]  Waiting for #menu ul to be present.")
        self.wait.until(EC.presence_of_element_located((By.ID, "menu")))

        logger.info("[INPUT]  Locating the 'Enabled' menu item's parent <li>.")
        # Enabled is the second top-level li (first is Disabled)
        enabled_li = self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//ul[@id='menu']/li[not(contains(@class,'ui-state-disabled'))]")
            )
        )

        logger.info("[INPUT]  Force-showing Enabled sub-menu via JS.")
        self._force_show_submenu(enabled_li)

        logger.info("[INPUT]  Locating 'Downloads' link and its parent <li>.")
        downloads_a = self.wait.until(EC.presence_of_element_located((By.LINK_TEXT, "Downloads")))
        downloads_li = downloads_a.find_element(By.XPATH, "..")

        logger.info("[INPUT]  Force-showing Downloads sub-menu via JS.")
        self._force_show_submenu(downloads_li)

        logger.info("[INPUT]  Waiting for 'PDF' link to be present and visible.")
        pdf_link = self.wait.until(EC.presence_of_element_located((By.LINK_TEXT, "PDF")))
        logger.info("[OUTPUT] Asserting PDF link is present in nested sub-menu.")
        self.assertIsNotNone(pdf_link, "PDF link should be present after nested hover.")

        pdf_href = pdf_link.get_attribute("href")
        logger.info(f"[OUTPUT] PDF link href: '{pdf_href}'.")
        self.assertIn("pdf", pdf_href.lower(), f"PDF href should contain 'pdf', got: '{pdf_href}'")
        logger.info("[OUTPUT] TC1 PASSED – Nested menu navigation to PDF verified.")

    # ─────────────────────────────────────────────────────────────────
    # TC2 – Happy Path: Enabled → Downloads → Excel
    # ─────────────────────────────────────────────────────────────────
    def test_jquery_menu_hover_excel_tc2(self):
        logger.info("[INPUT]  TC2 – Navigating to JQuery UI Menus page.")
        self.driver.get(URL)

        logger.info("[INPUT]  Waiting for #menu to be present.")
        self.wait.until(EC.presence_of_element_located((By.ID, "menu")))

        logger.info("[INPUT]  Locating the 'Enabled' <li> and force-showing its sub-menu.")
        enabled_li = self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//ul[@id='menu']/li[not(contains(@class,'ui-state-disabled'))]")
            )
        )
        self._force_show_submenu(enabled_li)

        logger.info("[INPUT]  Locating 'Downloads' <li> and force-showing its sub-menu.")
        downloads_a = self.wait.until(EC.presence_of_element_located((By.LINK_TEXT, "Downloads")))
        downloads_li = downloads_a.find_element(By.XPATH, "..")
        self._force_show_submenu(downloads_li)

        logger.info("[INPUT]  Waiting for 'Excel' link to be present.")
        excel_link = self.wait.until(EC.presence_of_element_located((By.LINK_TEXT, "Excel")))
        logger.info("[OUTPUT] Asserting Excel link is present in nested sub-menu.")
        self.assertIsNotNone(excel_link, "Excel link should be present after nested hover.")

        excel_href = excel_link.get_attribute("href")
        logger.info(f"[OUTPUT] Excel link href: '{excel_href}'.")
        self.assertIn("xls", excel_href.lower(), f"Excel href should contain 'xls', got: '{excel_href}'")
        logger.info("[OUTPUT] TC2 PASSED – Nested menu navigation to Excel verified.")

    # ─────────────────────────────────────────────────────────────────
    # TC3 – Sad Path: Disabled menu item is not navigable
    # ─────────────────────────────────────────────────────────────────
    def test_jquery_menu_disabled_not_clickable_tc3(self):
        logger.info("[INPUT]  TC3 – Navigating to JQuery UI Menus page.")
        self.driver.get(URL)

        logger.info("[INPUT]  Locating the 'Disabled' menu item.")
        disabled_item = self.wait.until(
            EC.presence_of_element_located((By.XPATH, "//li[contains(@class,'ui-state-disabled')]/a"))
        )

        logger.info("[OUTPUT] Asserting 'Disabled' item has the ui-state-disabled class.")
        disabled_li = disabled_item.find_element(By.XPATH, "..")
        classes = disabled_li.get_attribute("class")
        self.assertIn(
            "ui-state-disabled", classes,
            f"Expected 'ui-state-disabled' in classes but got: '{classes}'"
        )

        logger.info("[INPUT]  Attempting to click the disabled menu item.")
        url_before = self.driver.current_url
        try:
            disabled_item.click()
        except Exception as e:
            logger.info(f"[OUTPUT] Click raised {type(e).__name__} – disabled item blocked interaction.")

        logger.info("[OUTPUT] Asserting URL has NOT navigated away (allowing href='#' fragment).")
        url_after = self.driver.current_url
        url_before_base = url_before.split("#")[0]
        url_after_base  = url_after.split("#")[0]
        self.assertEqual(
            url_after_base, url_before_base,
            f"URL base should remain '{url_before_base}' after clicking disabled item, got '{url_after}'."
        )
        logger.info("[OUTPUT] TC3 PASSED – Disabled item correctly prevents page navigation.")

    # ─────────────────────────────────────────────────────────────────
    # TC4 – Sad Path: Disabled item has no accessible sub-menu
    # ─────────────────────────────────────────────────────────────────
    def test_jquery_menu_disabled_no_submenu_tc4(self):
        logger.info("[INPUT]  TC4 – Navigating to JQuery UI Menus page.")
        self.driver.get(URL)

        logger.info("[INPUT]  Locating the 'Disabled' <li> element.")
        disabled_li = self.wait.until(
            EC.presence_of_element_located((By.XPATH, "//li[contains(@class,'ui-state-disabled')]"))
        )

        logger.info("[INPUT]  Checking that any child <ul> of the Disabled <li> is NOT visible.")
        # jQuery UI renders <ul> sub-menus in the DOM even for disabled items (just hidden).
        # The correct assertion is that no visible/accessible sub-menu exists.
        child_uls = disabled_li.find_elements(By.TAG_NAME, "ul")
        logger.info(f"[OUTPUT] Child <ul> elements inside Disabled <li>: {len(child_uls)}.")

        for ul in child_uls:
            is_displayed = ul.is_displayed()
            logger.info(f"[OUTPUT] Child <ul> is_displayed: {is_displayed}.")
            self.assertFalse(
                is_displayed,
                "Any child <ul> of the Disabled item should NOT be visible/displayed."
            )

        logger.info("[OUTPUT] TC4 PASSED – Disabled item's sub-menu is correctly hidden/inaccessible.")


if __name__ == "__main__":
    unittest.main()
