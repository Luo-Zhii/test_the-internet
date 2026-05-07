# MASTER AUTOMATION TEST CASES

> **Project:** The Internet – Herokuapp Selenium Automation Suite
> **Framework:** Python · Selenium WebDriver · unittest
> **Total Features Covered:** 44
> **Last Updated:** 2026-05-07

---

## Feature: A/B Testing
> **File:** test_ab_testing.py

| Test Case ID | Method Name | Technique | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority |
|---|---|---|---|---|---|---|
| TC_AB_01 | `test_ab_testing_header_variation_tc1` | EP - Happy Path | Navigate to the A/B test page and verify that the page header reflects one of the two known valid experiment variants. | `Navigate to /abtest` → `Wait for EC.visibility_of_element_located((By.TAG_NAME, "h3"))` → `assertIn(text, VALID_HEADERS)` | The page header displays either "A/B Test Control" or "A/B Test Variation 1", confirming the experiment is running correctly. | High |
| TC_AB_02 | `test_ab_testing_paragraph_presence_tc2` | EP - Happy Path | Visit the A/B test page and confirm the informational description paragraph is always visible regardless of which variant is served. | `Navigate to /abtest` → `Wait for XPath //p[contains(text(),'Also known as split testing')]` → `assertTrue(paragraph.is_displayed())` | The paragraph describing split testing is visible and present on the page in all variants. | Medium |
| TC_AB_03 | `test_ab_testing_optout_cookie_tc3` | Negative Testing - Robustness | Set an opt-out cookie before loading the A/B test page and verify the system correctly removes the user from any experiment. | `Navigate to /abtest` → `add_cookie({'name': 'optimizelyOptOut', 'value': 'true'})` → `driver.refresh()` → `assertEqual(text, "No A/B Test")` | After the opt-out cookie is set, the page header shows "No A/B Test", confirming the user has been removed from all experiment variants. | High |
| TC_AB_04 | `test_ab_testing_reset_cookie_valid_variant_tc4` | BVA - Robustness | Repeat the cycle of clearing cookies and reloading the page 10 times to verify the system always returns a valid A/B variant and never crashes. | `Loop 10x: Navigate to /abtest` → `delete_all_cookies()` → `driver.refresh()` → `assertIn(text, VALID_HEADERS)` | Every single reload after a cookie reset returns a recognized A/B variant header, with no errors or unexpected states. | Medium |

---

## Feature: Add / Remove Elements
> **File:** test_add_remove_elements.py

| Test Case ID | Method Name | Technique | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority |
|---|---|---|---|---|---|---|
| TC_ARE_01 | `test_tc1_add_single_element` | EP - Happy Path | Click the "Add Element" button once and verify that exactly one delete button appears on the page. | `Navigate to /add_remove_elements/` → `Click XPath //button[text()='Add Element']` → `find_elements(By.CLASS_NAME, "added-manually")` → `assertEqual(len, 1)` | Exactly one "Delete" button is rendered and visible on the page after a single click. | High |
| TC_ARE_02 | `test_tc2_remove_single_element` | EP - Happy Path | Add one element and then immediately remove it, verifying the page returns to an empty state. | `Navigate` → `Click Add Element` → `Click Delete button` → `Wait for EC.staleness_of(delete_btn)` → `assertEqual(len(remaining), 0)` | After clicking delete, the button disappears and the page returns to a clean empty state. | High |
| TC_ARE_03 | `test_tc3_add_multiple_elements` | EP - Happy Path | Click "Add Element" five times in succession to verify the DOM correctly accumulates multiple dynamic elements. | `Navigate` → `Click Add Element 5×` → `Wait for EC.presence_of_all_elements_located(By.CLASS_NAME, "added-manually")` → `assertEqual(len, 5)` | Five distinct "Delete" buttons are generated, each visible and correctly appended to the page. | Medium |
| TC_ARE_04 | `test_tc4_remove_all_elements_dynamically` | BVA - Sad Path | Add three elements and then remove them one by one, verifying the DOM empties completely after each removal cycle. | `Navigate` → `Click Add Element 3×` → `For each btn: btn.click()` → `Wait for EC.staleness_of(btn)` → `assertEqual(len(remaining), 0)` | After removing all three elements, the page is completely empty with zero delete buttons remaining. | Medium |

---

## Feature: Basic Authentication
> **File:** test_basic_auth.py

| Test Case ID | Method Name | Technique | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority |
|---|---|---|---|---|---|---|
| TC_BA_01 | `test_tc1_success` | EP - Happy Path | Log in with the correct username and password via URL-based Basic Auth and verify the success message appears. | `Navigate to https://admin:admin@the-internet.herokuapp.com/basic_auth` → `find_element(By.TAG_NAME, "body")` → `assertTrue(is_authenticated())` | The congratulations message is displayed, confirming the user has been granted access. | Critical |
| TC_BA_02 | `test_tc2_wrong_password` | Negative Testing - Sad Path | Attempt to log in with a correct username but a wrong password and verify access is denied. | `Navigate to https://admin:wrongpassword@.../basic_auth` → `assertFalse(is_authenticated())` | The success message does not appear; the user is correctly blocked from accessing the secured page. | Critical |
| TC_BA_03 | `test_tc3_invalid_username` | Negative Testing - Sad Path | Attempt to log in with a non-existent username and verify the system rejects the request. | `Navigate to https://fakeuser:admin@.../basic_auth` → `assertFalse(is_authenticated())` | Authentication fails and the success message is absent, confirming the system validates username existence. | High |
| TC_BA_04 | `test_tc4_empty_both` | Negative Testing - Sad Path | Submit the authentication request with both the username and password fields completely empty. | `Navigate to https://:@.../basic_auth` → `assertFalse(is_authenticated())` | Access is denied when no credentials are provided, and no success message is shown. | High |
| TC_BA_05 | `test_tc5_case_sensitivity_user` | Negative Testing - Edge Case | Attempt to log in using a username with incorrect capitalisation (e.g., "Admin" instead of "admin") to confirm the system is case-sensitive. | `Navigate to https://Admin:admin@.../basic_auth` → `assertFalse(is_authenticated())` | The system rejects the mixed-case username, confirming that authentication is case-sensitive for usernames. | Medium |
| TC_BA_06 | `test_tc6_case_sensitivity_pass` | Negative Testing - Edge Case | Attempt to log in with a password in all uppercase letters to confirm the password field is also case-sensitive. | `Navigate to https://admin:ADMIN@.../basic_auth` → `assertFalse(is_authenticated())` | The system rejects the uppercase password, confirming that authentication is case-sensitive for passwords. | Medium |
| TC_BA_07 | `test_tc7_special_chars_password` | Negative Testing - Robustness | Attempt login with a password containing special characters (e.g., "@", ":") to verify the URL encoding mechanism handles them safely without crashing. | `urllib.parse.quote("p@ss:word#123")` → `Navigate to encoded URL` → `Log result without assertion block` | The application handles the special-character password gracefully via URL encoding, without throwing an unhandled error. | Medium |
| TC_BA_08 | `test_tc8_sql_injection_attempt` | Security Testing - Robustness | Inject a basic SQL injection string as the username to verify the authentication layer is not vulnerable to this attack. | `urllib.parse.quote("' OR '1'='1")` → `Navigate` → `assertFalse(is_authenticated())` | The SQL injection string is treated as a literal invalid credential and access is denied, confirming the system is not vulnerable. | High |
| TC_BA_09 | `test_tc9_very_long_credentials` | Negative Testing - Robustness | Submit an extremely long string (1000 characters) as both username and password to test for buffer overflow vulnerabilities. | `long_str = "a" * 1000` → `Navigate to encoded URL` → `assertFalse(is_authenticated())` | The system handles the oversized credentials gracefully and denies access, without crashing or hanging. | Medium |

---

## Feature: Broken Images
> **File:** test_broken_images.py

| Test Case ID | Method Name | Technique | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority |
|---|---|---|---|---|---|---|
| TC_BI_01 | `test_tc1_verify_total_images_on_page` | EP - Happy Path | Load the broken images page and verify that at least three image elements are present in the page layout. | `Navigate to /broken_images` → `Wait for EC.presence_of_all_elements_located(By.TAG_NAME, "img")` → `assertTrue(len(images) >= 3)` | At least three image elements are found in the page DOM, confirming the basic structure is intact. | Medium |
| TC_BI_02 | `test_tc2_identify_broken_images` | EP - Sad Path | Perform an HTTP request for each image source URL and identify exactly which images return a non-200 status code. | `find_elements(By.TAG_NAME, "img")` → `For each: requests.get(src, timeout=5)` → `assertEqual(len(broken_imgs), 2)` | Exactly two images are identified as broken (non-200 HTTP response), matching the known defects on this demo page. | High |
| TC_BI_03 | `test_tc3_identify_valid_images` | EP - Happy Path | Verify that the script correctly identifies images that load successfully (HTTP 200 OK). | `find_elements(By.TAG_NAME, "img")` → `For each: requests.get(src)` → `assertTrue(len(valid_imgs) >= 1)` | At least one image on the page successfully returns a 200 OK response and is identified as a valid, working image. | Medium |

---

## Feature: Challenging DOM
> **File:** test_challenging_dom.py

| Test Case ID | Method Name | Technique | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority |
|---|---|---|---|---|---|---|
| TC_CD_01 | `test_dynamic_buttons_tc1` | EP - Happy Path | Click the red alert button on the page (which has a dynamically changing ID) using a stable CSS class selector, and verify it remains visible after the DOM reloads. | `Navigate to /challenging_dom` → `Click CSS_SELECTOR ".button.alert"` → `Wait for EC.presence_of_element_located(".button.alert")` → `assertTrue(is_displayed())` | The red button is found and clickable without relying on a volatile ID, and it remains visible after the post-click DOM refresh. | High |
| TC_CD_02 | `test_table_ep_mid_tc2` | EP - Happy Path | Read and verify the data content from the 5th row (middle) of the table to confirm the data grid renders correctly. | `Navigate to /challenging_dom` → `Wait for XPath //table/tbody/tr[5]` → `assertTrue("Iuvaret4" in text or "Apeirian4" in text)` | Row 5 contains non-empty text with the expected middle-range data values ("Iuvaret4" or "Apeirian4"). | Medium |
| TC_CD_03 | `test_table_bva_min_tc3` | BVA - Happy Path | Read and verify the content from the 1st row (minimum boundary) of the data table. | `Navigate to /challenging_dom` → `Wait for XPath //table/tbody/tr[1]` → `assertTrue("Iuvaret0" in text or "Apeirian0" in text)` | The first row contains the expected minimum-index data values, confirming the table renders correctly from the top. | Medium |
| TC_CD_04 | `test_table_bva_max_tc4` | BVA - Happy Path | Read and verify the content from the 10th row (maximum boundary) of the data table. | `Navigate to /challenging_dom` → `Wait for XPath //table/tbody/tr[10]` → `assertTrue("Iuvaret9" in text or "Apeirian9" in text)` | The last row contains the expected maximum-index data values, confirming the table renders all 10 rows correctly. | Medium |
| TC_CD_05 | `test_table_negative_out_of_bounds_tc5` | Negative Testing - Sad Path | Attempt to access a non-existent 11th table row and verify the system gracefully handles the missing element without crashing. | `WebDriverWait(driver, 2)` → `Try to locate XPath //table/tbody/tr[11]` → `Catch TimeoutException or NoSuchElementException` | A timeout or element-not-found exception is caught gracefully, confirming the table has exactly 10 rows and no more. | Medium |
| TC_CD_06 | `test_canvas_verification_tc6` | EP - Happy Path | Verify that the HTML canvas element is present and visible on the challenging DOM page. | `Navigate to /challenging_dom` → `Wait for CSS_SELECTOR "canvas#canvas"` → `assertTrue(canvas.is_displayed())` | The canvas element is rendered and visible on the page, confirming the dynamic rendering engine functions correctly. | Low |
| TC_CD_07 | `test_table_action_links_tc7` | EP - Happy Path | Click the "edit" and "delete" action links in a specific table row and verify each click correctly updates the browser's URL fragment. | `Click XPath //table/tbody/tr[3]/td[7]/a[@href='#edit']` → `assertIn("#edit", current_url)` → `Click a[@href='#delete']` → `assertIn("#delete", current_url)` | After each click, the URL fragment updates to "#edit" and then "#delete", confirming the action links are functional. | Medium |
| TC_CD_08 | `test_tc8_dynamic_id_shift` | EP - Robustness | Capture the ID of the blue button before clicking it, then verify the ID has changed after the page dynamically reloads, proving the DOM is truly volatile. | `Locate ".button:not(.alert):not(.success)"` → `old_id = get_attribute("id")` → `Click` → `Wait for EC.staleness_of()` → `new_id = get_attribute("id")` → `assertNotEqual(old_id, new_id)` | The button's ID value is different before and after the click, confirming that the page uses dynamically generated element IDs. | High |

---

## Feature: Checkboxes
> **File:** test_checkbox.py

| Test Case ID | Method Name | Technique | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority |
|---|---|---|---|---|---|---|
| TC_CB_01 | `test_tc1_default_state_validation` | EP - Happy Path | Load the checkboxes page and verify the factory-default states: the first checkbox is unchecked and the second is checked. | `Navigate to /checkboxes` → `XPath //*[@id="checkboxes"]/input[1]` and `input[2]` → `assertFalse(cb1.is_selected())` → `assertTrue(cb2.is_selected())` | Checkbox 1 is unchecked and Checkbox 2 is checked by default, exactly as the page is designed. | High |
| TC_CB_02 | `test_tc2_check_first_checkbox` | EP - Happy Path | Interact with the initially unchecked first checkbox by clicking it, then verify it is now in the checked state. | `Navigate to /checkboxes` → `If not cb1.is_selected(): cb1.click()` → `assertTrue(cb1.is_selected())` | The first checkbox transitions from unchecked to checked after being clicked. | High |
| TC_CB_03 | `test_tc3_uncheck_second_checkbox` | EP - Happy Path | Interact with the initially checked second checkbox by clicking it, then verify it moves to the unchecked state. | `Navigate to /checkboxes` → `If cb2.is_selected(): cb2.click()` → `assertFalse(cb2.is_selected())` | The second checkbox transitions from checked to unchecked after being clicked. | High |
| TC_CB_04 | `test_tc4_toggle_both_checkboxes` | Negative Testing - Robustness | Repeatedly toggle both checkboxes back and forth to verify the checked/unchecked state remains reliable and consistent. | `cb1.click()` → `assertTrue(cb1)` → `cb1.click()` → `assertFalse(cb1)` → Repeat for `cb2` | Both checkboxes correctly toggle between checked and unchecked states across multiple consecutive clicks with no state corruption. | Medium |

---

## Feature: Context Menu
> **File:** test_context_menu.py

| Test Case ID | Method Name | Technique | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority |
|---|---|---|---|---|---|---|
| TC_CM_01 | `test_tc1_context_menu_success_and_cleanup` | EP - Happy Path | Right-click inside the designated hot-spot area and verify that the correct JavaScript alert message appears, then dismiss it cleanly. | `Navigate to /context_menu` → `ActionChains.context_click(#hot-spot)` → `Wait for EC.alert_is_present()` → `assertEqual(alert.text, "You selected a context menu")` → `alert.accept()` | The alert message reads "You selected a context menu" and is successfully dismissed without leaving any residual state. | High |
| TC_CM_02 | `test_tc2_left_click_ignores_menu` | Negative Testing - Sad Path | Perform a standard left-click (instead of a right-click) on the hot-spot and verify that no JavaScript alert is triggered. | `Navigate to /context_menu` → `ActionChains.click(#hot-spot)` → `WebDriverWait(driver, 2)` → `Catch TimeoutException` | No alert is triggered by a standard left-click, confirming the feature is correctly bound only to the right-click event. | Medium |
| TC_CM_03 | `test_tc3_boundary_click_outside_hotspot` | BVA - Robustness | Right-click outside the designated hot-spot area (on the page heading) and verify that no alert is incorrectly triggered. | `Navigate to /context_menu` → `ActionChains.context_click(By.TAG_NAME, "h3")` → `WebDriverWait(driver, 2)` → `Catch TimeoutException` | No alert appears when right-clicking outside the hot-spot, confirming the event listener is correctly scoped to the designated area only. | Medium |

---

## Feature: Digest Authentication
> **File:** test_digest_auth.py

| Test Case ID | Method Name | Technique | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority |
|---|---|---|---|---|---|---|
| TC_DA_01 | `test_digest_auth_happy_path_tc1` | EP - Happy Path | Log in to the Digest Auth-protected page using valid credentials and verify the success confirmation message appears. | `urllib.parse.quote("admin")` + `urllib.parse.quote("admin")` → `Navigate to https://admin:admin@.../digest_auth` → `Wait for XPath //p[contains(text(),'Congratulations')]` | The "Congratulations! You must have the proper credentials." message is visible, confirming successful Digest Authentication. | Critical |
| TC_DA_02 | `test_digest_auth_invalid_creds_tc2` | Negative Testing - Sad Path | Attempt to access the Digest Auth page with an incorrect password and verify the page is denied. | `Navigate to https://admin:wrong@.../digest_auth` → `_assert_success_absent(timeout=2)` → `assertNotIn(SUCCESS_TEXT, body_text)` | The success message does not appear; the incorrect password is correctly rejected by the Digest Authentication protocol. | Critical |
| TC_DA_03 | `test_digest_auth_unauthorized_tc3` | Security Testing - Sad Path | Attempt to access the Digest Auth page with no credentials at all in the URL and verify access is blocked. | `Navigate to https://the-internet.herokuapp.com/digest_auth` (no credentials)` → `_assert_success_absent(timeout=2)` | Access is denied and no success message appears, confirming the endpoint is properly protected and not accessible without credentials. | Critical |
| TC_DA_04 | `test_digest_auth_special_chars_tc4` | Negative Testing - Robustness | Test that a password containing a special character "@" is safely URL-encoded before transmission and results in a correct rejection. | `urllib.parse.quote("admin@123", safe="")` → `assertIn("%40", encoded_pass)` → `Navigate to constructed URL` → `_assert_success_absent(timeout=2)` | The "@" character is correctly percent-encoded as "%40" in the URL. The password is safely transmitted and the invalid credential is correctly rejected. | High |

---

## Feature: Disappearing Elements
> **File:** test_disappearing_elements.py

| Test Case ID | Method Name | Technique | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority |
|---|---|---|---|---|---|---|
| TC_DE_01 | `test_tc1_verify_permanent_links` | EP - Happy Path | Load the page and confirm that all four permanent navigation links (Home, About, Contact Us, Portfolio) are always visible. | `Navigate to /disappearing_elements` → `For each text in ["Home","About","Contact Us","Portfolio"]: Wait for EC.presence_of_element_located(By.LINK_TEXT, text)` → `assertTrue(is_displayed())` | All four permanent navigation links are present and visible on every page load without exception. | High |
| TC_DE_02 | `test_tc2_gallery_appears_on_refresh` | EP - Robustness | Refresh the page up to five times to catch the randomly appearing "Gallery" link, click it, and confirm it leads to a 404 page. | `Loop up to 5×: driver.refresh()` → `find_elements(By.LINK_TEXT, "Gallery")` → `If found: click()` → `assertIn("Not Found", page_source)` | The "Gallery" link is eventually detected across multiple refreshes, is clickable, and correctly navigates to a 404 Not Found page. | Medium |

---

## Feature: Drag and Drop
> **File:** test_drag_and_drop.py

| Test Case ID | Method Name | Technique | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority |
|---|---|---|---|---|---|---|
| TC_DD_01 | `test_tc1_drag_a_to_b` | EP - Happy Path | Drag Block A onto Block B and verify that the two blocks visually swap their labels ("A" becomes "B" and vice versa). | `Navigate to /drag_and_drop` → `helper_html5_drag_and_drop(col_a, col_b)` via JS event simulation → `assertEqual(col_a.text, "B")` and `assertEqual(col_b.text, "A")` | After dragging A onto B, Block A's label displays "B" and Block B's label displays "A", confirming the swap was successful. | High |
| TC_DD_02 | `test_tc2_drag_b_to_a` | EP - Robustness | Perform a full drag-and-drop cycle: drag A onto B, then drag B back onto A, and verify both blocks return to their original positions. | `helper_html5_drag_and_drop(col_a, col_b)` → `helper_html5_drag_and_drop(col_b, col_a)` → `assertEqual(col_a.text, "A")` and `assertEqual(col_b.text, "B")` | After two drag operations, both blocks return to their original labels ("A" and "B"), confirming the swap mechanism is fully reversible. | Medium |

---

## Feature: Dropdown
> **File:** test_dropdown.py

| Test Case ID | Method Name | Technique | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority |
|---|---|---|---|---|---|---|
| TC_DR_01 | `test_tc1_default_placeholder` | EP - Happy Path | Load the dropdown page and verify the default state: the placeholder option is selected and cannot be manually chosen by a user. | `Navigate to /dropdown` → `Select(By.ID, "dropdown")` → `assertEqual(first_selected_option.text, "Please select an option")` → `assertFalse(first_option.is_enabled())` | The dropdown shows 3 options, the placeholder "Please select an option" is selected by default, and it is disabled to prevent re-selection. | High |
| TC_DR_02 | `test_tc2_select_option_1` | EP - Happy Path | Select "Option 1" from the dropdown by index and verify the selection is reflected correctly. | `Navigate to /dropdown` → `Select(By.ID, "dropdown")` → `select_by_index(1)` → `assertEqual(first_selected_option.text, "Option 1")` | "Option 1" is successfully selected and shown as the current value of the dropdown. | High |
| TC_DR_03 | `test_tc3_select_option_2` | EP - Happy Path | Select "Option 2" from the dropdown using its visible text and confirm it becomes the active selection. | `Navigate to /dropdown` → `select_by_visible_text("Option 2")` → `assertEqual(first_selected_option.text, "Option 2")` | "Option 2" is successfully selected by visible text and is displayed as the active dropdown value. | High |
| TC_DR_04 | `test_tc4_switch_between_options` | EP - Robustness | Switch from "Option 1" to "Option 2" using value-based selection and verify the dropdown correctly reflects the override. | `select_by_value("1")` → `assertEqual(..., "Option 1")` → `select_by_value("2")` → `assertEqual(..., "Option 2")` | The dropdown correctly changes from "Option 1" to "Option 2", proving that selecting a new value always overrides the previous selection. | Medium |

---

## Feature: Dynamic Content
> **File:** test_dynamic_content.py

| Test Case ID | Method Name | Technique | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority |
|---|---|---|---|---|---|---|
| TC_DC_01 | `test_tc1_content_structure_intact` | EP - Happy Path | Load the dynamic content page and verify exactly 3 rows of content (image + text block) are always rendered. | `Navigate to /dynamic_content` → `find_elements(By.CSS_SELECTOR, "#content > .row:not(.large-centered)")` → `assertEqual(len(images), 3)` | Exactly 3 image-text row pairs are present on every page load, confirming the content structure is consistent. | Medium |
| TC_DC_02 | `test_tc2_content_changes_on_refresh` | EP - Robustness | Refresh the page up to 3 times and verify that at least some content (images or text) changes between loads, confirming randomization is active. | `get_content_state()` before → `driver.refresh()` up to 3× → `get_content_state()` after → `assertNotEqual(initial, refreshed)` | At least one content element differs between the initial load and a subsequent refresh, proving the page is genuinely dynamic. | Medium |
| TC_DC_03 | `test_tc3_static_content_parameter` | EP - Robustness | Navigate with the `?with_content=static` query parameter and verify the first two rows remain identical across page refreshes. | `Navigate to /dynamic_content?with_content=static` → `get_content_state()` → `driver.refresh()` → `assertEqual(initial_images[:2], refreshed_images[:2])` | The first two content rows are identical before and after refresh when the static parameter is applied, confirming the parameter works correctly. | Low |

---

## Feature: Dynamic Controls
> **File:** test_dynamic_controls.py

| Test Case ID | Method Name | Technique | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority |
|---|---|---|---|---|---|---|
| TC_DCT_01 | `test_tc1_checkbox_removal` | EP - Happy Path | Click the "Remove" button and wait for the checkbox to completely disappear from the page, then verify the confirmation message. | `Navigate to /dynamic_controls` → `Click #checkbox-example > button` → `Wait for EC.staleness_of(checkbox)` → `assertEqual(msg.text, "It's gone!")` → `assertEqual(len(find_elements(By.ID,"checkbox")), 0)` | The checkbox is fully removed from the page DOM and the "It's gone!" message is displayed. | High |
| TC_DCT_02 | `test_tc2_checkbox_addition` | EP - Happy Path | Remove the checkbox first, then click "Add" to restore it, verifying the DOM re-includes it and the correct message is shown. | `Click Remove` → `Wait for message` → `Click Add` → `Wait for EC.presence_of_element_located(By.ID, "checkbox")` → `assertEqual(msg.text, "It's back!")` | The checkbox is successfully re-added to the page and the "It's back!" confirmation message is displayed. | High |
| TC_DCT_03 | `test_tc3_input_enable` | EP - Happy Path | Click the "Enable" button and wait for the text input field to become interactive, then verify the confirmation message. | `Navigate to /dynamic_controls` → `assertFalse(input_field.is_enabled())` → `Click Enable button` → `Wait for EC.element_to_be_clickable(input)` → `assertEqual(msg.text, "It's enabled!")` | The text input field transitions from disabled to enabled and the "It's enabled!" message confirms the state change. | High |
| TC_DCT_04 | `test_tc4_input_disable` | EP - Happy Path | Enable the input field first, then click "Disable" and wait for the field to return to a non-interactive state. | `Click Enable` → `Wait for clickable` → `Click Disable` → `Wait for lambda: not input_field.is_enabled()` → `assertEqual(msg.text, "It's disabled!")` | The input field transitions back to a disabled (non-interactive) state and the "It's disabled!" message is shown. | High |

---

## Feature: Dynamic Loading
> **File:** test_dynamic_loading.py

| Test Case ID | Method Name | Technique | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority |
|---|---|---|---|---|---|---|
| TC_DL_01 | `test_hidden_element_ep_tc1` | EP - Happy Path | Click the Start button on Example 1, wait for the loading bar to finish, and verify the hidden "Hello World!" message becomes visible. | `Navigate to /dynamic_loading/1` → `Click #start button` → `Wait for EC.invisibility_of_element_located(By.ID, "loading")` → `assertEqual(finish.text, "Hello World!")` | The "Hello World!" text is revealed after the loading animation completes, confirming the hidden-element reveal mechanism works. | Critical |
| TC_DL_02 | `test_rendered_element_ep_tc2` | EP - Happy Path | Click the Start button on Example 2, wait for the loading bar, and verify the element is dynamically rendered into the DOM with the correct text. | `Navigate to /dynamic_loading/2` → `Click #start button` → `Wait for EC.invisibility_of_element_located(By.ID, "loading")` → `assertEqual(finish.text, "Hello World!")` | The "Hello World!" element is injected into the DOM and displayed correctly after the loading process completes. | Critical |
| TC_DL_03 | `test_double_click_sad_path_tc3` | Negative Testing - Robustness | Rapidly double-click the Start button and verify the page recovers gracefully and still shows the correct result without corruption. | `Navigate to /dynamic_loading/1` → `Click Start` → `Try second click immediately` → `Wait for invisibility of #loading` → `assertEqual(finish.text, "Hello World!")` | Despite the rapid double-click, the page recovers and correctly displays "Hello World!" without errors or a broken state. | Medium |
| TC_DL_04 | `test_missing_element_sad_path_tc4` | Negative Testing - Sad Path | Attempt to locate a button using a completely wrong CSS selector and verify a timeout exception is raised as expected. | `Navigate to /dynamic_loading/1` → `WebDriverWait(driver, 10).until(EC.element_to_be_clickable(By.CSS_SELECTOR, "button#wrong-id"))` → `Catch TimeoutException` | A TimeoutException is raised because the invalid selector matches nothing, confirming the test correctly validates element presence. | Medium |
| TC_DL_05 | `test_short_timeout_bva_tc5` | BVA - Sad Path | Use a 0.5-second timeout (far below the loading duration) to verify the loading bar cannot possibly complete in that boundary window. | `Navigate to /dynamic_loading/1` → `Click Start` → `WebDriverWait(driver, 0.5).until(EC.invisibility_of_element_located(By.ID, "loading"))` → `Catch TimeoutException` | A TimeoutException is correctly raised because the loading bar persists beyond the 0.5-second boundary, confirming the animation takes longer than the minimum threshold. | Medium |

---

## Feature: Entry Ad (Modal)
> **File:** test_entry_ad.py

| Test Case ID | Method Name | Technique | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority |
|---|---|---|---|---|---|---|
| TC_EA_01 | `test_tc1_close_entry_ad_modal` | EP - Happy Path | Open the page, clear cookies to force the ad to appear, and verify the modal can be closed successfully. | `Navigate to /entry_ad` → `delete_all_cookies()` → `driver.refresh()` → `Wait for EC.visibility_of_element_located(By.ID, "modal")` → `execute_script click .modal-footer p` → `Wait for EC.invisibility_of_element_located(By.ID, "modal")` | The entry ad modal appears on page load and can be dismissed successfully, disappearing from the viewport. | High |
| TC_EA_02 | `test_tc2_ad_does_not_reappear_on_refresh` | EP - Robustness | Dismiss the modal once, then refresh the page while retaining the session cookie, and confirm the ad does not reappear. | `Dismiss modal` → `driver.refresh()` → `WebDriverWait(driver, 3).until(visibility_of(By.ID, "modal"))` → `Catch exception (expected)` | After the initial dismissal, the modal does not reappear on the next page refresh, confirming the cookie-based suppression works correctly. | High |
| TC_EA_03 | `test_tc3_ad_reappears_on_cleared_cookies` | EP - Robustness | Dismiss the modal, clear all cookies, refresh, and verify the ad reappears as if it's the user's first visit. | `Dismiss modal` → `delete_all_cookies()` → `driver.refresh()` → `Wait for EC.visibility_of_element_located(By.ID, "modal")` | The entry ad modal reappears after cookies are cleared, confirming the system correctly uses cookies to track whether a user has already seen the ad. | Medium |

---

## Feature: Exit Intent
> **File:** test_exit_intent.py

| Test Case ID | Method Name | Technique | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority |
|---|---|---|---|---|---|---|
| TC_EI_01 | `test_exit_intent_happy_path_tc1` | EP - Happy Path | Simulate the user's mouse leaving the browser viewport, verify the exit-intent modal appears with the correct title, then close it. | `Navigate to /exit_intent` → `execute_script: document.documentElement.dispatchEvent(new MouseEvent('mouseleave'))` → `Wait for .modal` → `assertEqual(h3.text, "THIS IS A MODAL WINDOW")` → `Click .modal-footer p` | The modal appears with the title "THIS IS A MODAL WINDOW" when the exit intent is triggered, and it closes correctly when dismissed. | High |
| TC_EI_02 | `test_exit_intent_one_time_trigger_tc2` | EP - Robustness | Trigger and dismiss the modal, then trigger the exit intent a second time and verify the modal does not re-appear (one-time logic). | `_trigger_exit_intent()` → `Dismiss modal` → `_trigger_exit_intent()` again → `WebDriverWait(driver, 3)` → `Catch TimeoutException` | The modal correctly suppresses itself after the first dismissal and does not reappear on a second exit-intent trigger within the same session. | Medium |
| TC_EI_03 | `test_exit_intent_no_trigger_within_bounds_tc3` | Negative Testing - Sad Path | Move the mouse within the valid page area (not outside the viewport) and verify this normal movement does not trigger the exit-intent modal. | `Navigate to /exit_intent` → `ActionChains.move_to_element(body).move_by_offset(100, 100).perform()` → `WebDriverWait(driver, 2)` → `Catch TimeoutException` | Moving the mouse within the page boundaries does not trigger the exit-intent modal, confirming it is only activated by leaving the viewport. | Medium |
| TC_EI_04 | `test_exit_intent_overlay_blocking_tc4` | Negative Testing - Security | Trigger the exit-intent modal and then attempt to click a background link through the modal overlay, verifying the overlay correctly blocks interaction. | `_trigger_exit_intent()` → `Wait for .modal` → `footer_link.click()` → `Catch ElementClickInterceptedException` | The modal overlay prevents any background elements from being clickable while active, confirming the security behaviour of the modal is correct. | High |

---

## Feature: File Download
> **File:** test_file_download.py

| Test Case ID | Method Name | Technique | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority |
|---|---|---|---|---|---|---|
| TC_FD_01 | `test_tc1_download_success` | EP - Happy Path | Click the first available downloadable file link and verify the file physically appears in the configured download directory on the local filesystem. | `Navigate to /download` → `find_elements(By.CSS_SELECTOR, ".example a")[0].click()` → `Poll os.path.exists(file_path)` for up to 10 seconds | The downloaded file is found in the test_downloads directory within 10 seconds, confirming the download completed successfully. | High |

---

## Feature: File Upload
> **File:** test_file_upload.py

| Test Case ID | Method Name | Technique | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority |
|---|---|---|---|---|---|---|
| TC_FU_01 | `test_tc1_upload_valid_file` | EP - Happy Path | Create a temporary text file, upload it via the file input element, and verify the success message appears after submission. | `Navigate to /upload` → `Create temp file` → `find_element(By.ID, "file-upload").send_keys(file_path)` → `Click #file-submit` → `assertEqual(h3.text, "File Uploaded!")` | The "File Uploaded!" success heading is displayed after submitting a valid file, confirming the upload pipeline works end-to-end. | High |
| TC_FU_02 | `test_tc2_upload_empty_submission` | Negative Testing - Sad Path | Submit the upload form without selecting any file and verify the system returns an appropriate server error response. | `Navigate to /upload` → `find_element(By.ID, "file-submit").click()` (no file selected) → `assertEqual(h1.text, "Internal Server Error")` | The server returns a 500 Internal Server Error when no file is attached to the upload submission, confirming the endpoint validates file presence. | High |

---

## Feature: Floating Menu
> **File:** test_floating_menu.py

| Test Case ID | Method Name | Technique | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority |
|---|---|---|---|---|---|---|
| TC_FM_01 | `test_tc1_menu_visible_top` | EP - Happy Path | Load the floating menu page and verify the navigation menu is visible at the top without any scrolling. | `Navigate to /floating_menu` → `Wait for EC.visibility_of_element_located(By.ID, "menu")` → `assertTrue(menu.is_displayed())` | The floating navigation menu is visible immediately upon page load, before any user interaction. | Medium |
| TC_FM_02 | `test_tc2_menu_visible_on_scroll` | EP - Robustness | Scroll the page all the way to the bottom and verify the floating menu is still visible and its links remain accessible. | `Navigate to /floating_menu` → `execute_script("window.scrollTo(0, document.body.scrollHeight)")` → `assertTrue(menu.is_displayed())` → `assertTrue(home_link.is_displayed() and about_link.is_displayed())` | The floating menu remains visible and its links (Home, About) are still displayed even when the page is scrolled to the very bottom. | High |
| TC_FM_03 | `test_tc3_menu_anchor_links_work` | EP - Happy Path | Click the "Home" link in the floating menu and verify the page URL is updated with the correct anchor hash. | `Navigate to /floating_menu` → `Wait for EC.element_to_be_clickable(By.LINK_TEXT, "Home")` → `click()` → `assertIn("#home", driver.current_url)` | Clicking the "Home" link updates the URL to include the "#home" fragment, confirming the anchor navigation is functional. | Medium |

---

## Feature: Forgot Password
> **File:** test_forgot_password.py

| Test Case ID | Method Name | Technique | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority |
|---|---|---|---|---|---|---|
| TC_FP_01 | `test_tc1_valid_email_submission` | EP - Happy Path | Submit a properly formatted email address to the Forgot Password form and verify the system handles the request without an unexpected crash. | `Navigate to /forgot_password` → `find_element(By.ID, "email").send_keys("test_user_valid@example.com")` → `Click #form_submit` → `Wait for page navigation` | The system either shows a success message or returns the known 500 error from this demo endpoint, but does not crash unexpectedly. | Medium |
| TC_FP_02 | `test_tc2_empty_email_submission` | Negative Testing - Sad Path | Submit the form with the email field completely empty and verify the server returns an error response. | `Navigate to /forgot_password` → `Click #form_submit` (no email entered) → `assertIn("Internal Server Error", result_text)` | An "Internal Server Error" is returned for an empty submission, confirming the endpoint validates the email field presence. | Medium |
| TC_FP_03 | `test_tc3_invalid_email_format` | Negative Testing - Sad Path | Enter a malformed string (no "@" or domain) as the email and verify the system responds with an error rather than a success. | `Navigate to /forgot_password` → `send_keys("user_without_at_symbol_or_domain")` → `Click #form_submit` → `assertTrue("Internal Server Error" in result or "Your e-mail's been sent!" in result)` | The malformed email is handled without an unexpected crash, returning either a server error or the known demo success message. | Low |

---

## Feature: Form Authentication (Login)
> **File:** test_form_authentication.py

| Test Case ID | Method Name | Technique | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority |
|---|---|---|---|---|---|---|
| TC_FA_01 | `test_tc1_login_success` | EP - Happy Path | Log in with fully valid credentials and verify the user is redirected to the secure area with a success flash message. | `Navigate to /login` → `send_keys("tomsmith") to #username` → `send_keys("SuperSecretPassword!") to #password` → `Click button[type='submit']` → `assertIn("/secure", current_url)` → `assertIn("You logged into a secure area!", flash)` | The user is redirected to `/secure` and the flash message "You logged into a secure area!" is displayed. | Critical |
| TC_FA_02 | `test_tc2_invalid_password` | Negative Testing - Sad Path | Attempt login with the correct username but a wrong password and verify the appropriate error flash is shown. | `helper_login("tomsmith", "wrongpassword")` → `assertIn("Your password is invalid!", get_flash_msg())` | The "Your password is invalid!" flash message is displayed and the user remains on the login page. | Critical |
| TC_FA_03 | `test_tc3_invalid_username` | Negative Testing - Sad Path | Attempt login with a non-existent username and verify the system returns the correct username error. | `helper_login("wronguser", "SuperSecretPassword!")` → `assertIn("Your username is invalid!", get_flash_msg())` | The "Your username is invalid!" flash message is displayed, confirming the system validates username existence first. | Critical |
| TC_FA_04 | `test_tc4_empty_credentials` | Negative Testing - Sad Path | Submit the login form with both username and password fields completely empty. | `helper_login("", "")` → `assertIn("Your username is invalid!", get_flash_msg())` | The system correctly rejects the empty submission and shows the "Your username is invalid!" error message. | High |
| TC_FA_05 | `test_tc5_empty_password` | Negative Testing - Sad Path | Provide a valid username but leave the password field completely empty, then submit. | `helper_login("tomsmith", "")` → `assertIn("Your password is invalid!", get_flash_msg())` | The "Your password is invalid!" flash message is shown, confirming the system validates both fields independently. | High |
| TC_FA_06 | `test_tc6_empty_username` | Negative Testing - Sad Path | Leave the username field empty while providing the correct password, then submit. | `helper_login("", "SuperSecretPassword!")` → `assertIn("Your username is invalid!", get_flash_msg())` | The "Your username is invalid!" message appears, confirming username is validated before the password. | High |
| TC_FA_07 | `test_tc7_logout_functionality` | EP - Happy Path | Log in successfully, then click the logout button and verify the user is redirected back to the login page with a logout confirmation message. | `helper_login("tomsmith", "SuperSecretPassword!")` → `Click a.button.secondary` → `Wait for EC.url_contains("/login")` → `assertIn("You logged out of the secure area!", flash)` | The user is redirected to `/login` and the "You logged out of the secure area!" flash message confirms a successful logout. | Critical |
| TC_FA_08 | `test_tc8_case_sensitive_username` | Negative Testing - Edge Case | Attempt login with the username using mixed/wrong capitalisation (e.g., "TomSmith") to verify case sensitivity. | `helper_login("TomSmith", "SuperSecretPassword!")` → `assertIn("Your username is invalid!", get_flash_msg())` | Authentication fails for the incorrectly capitalised username, confirming the system is case-sensitive for usernames. | Medium |
| TC_FA_09 | `test_tc9_case_sensitive_password` | Negative Testing - Edge Case | Attempt login with the password in all lowercase letters to verify the password field is case-sensitive. | `helper_login("tomsmith", "supersecretpassword!")` → `assertIn("Your password is invalid!", get_flash_msg())` | Authentication fails for the all-lowercase password, confirming the system is case-sensitive for passwords. | Medium |
| TC_FA_10 | `test_tc10_special_characters` | Security Testing - Robustness | Enter a username composed entirely of special characters and verify the system rejects it safely without crashing. | `helper_login("!@#$%^&*", "SuperSecretPassword!")` → `assertIn("Your username is invalid!", get_flash_msg())` | The special-character username is rejected with the standard invalid username message, confirming no injection vulnerability exists. | Medium |


---

## Feature: iFrame & Frames
> **File:** test_frame.py

| Test Case ID | Method Name | Technique | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority |
|---|---|---|---|---|---|---|
| TC_IF_01 | `test_iframe_happy_path_tc1` | EP - Happy Path | Switch the browser context into the TinyMCE iFrame, inject text into the editor, and verify the content is correctly written. | `Navigate to /iframe` → `Wait for EC.frame_to_be_available_and_switch_to_it(By.ID, "mce_0_ifr")` → `execute_script set innerText on #tinymce` → `assertEqual(editor.text, "Happy Path Test")` | The text "Happy Path Test" is successfully written into the iFrame's editor and confirmed by reading back the element's text. | High |
| TC_IF_02 | `test_nested_frames_happy_path_tc2` | EP - Happy Path | Navigate through two levels of nested frames (root → frame-top → frame-middle) and verify the correct content is found in the deepest frame. | `Navigate to /nested_frames` → `switch_to.frame("frame-top")` → `switch_to.frame("frame-middle")` → `assertEqual(content.text.strip(), "MIDDLE")` | The text "MIDDLE" is correctly found inside the deepest targeted frame, confirming the multi-level frame traversal works correctly. | High |
| TC_IF_03 | `test_frame_context_leak_sad_path_tc3` | Negative Testing - Sad Path | After switching into an iFrame, attempt to find a main-page element and verify the browser context is correctly isolated within the frame. | `switch_to.frame("mce_0_ifr")` → `try find_element(By.TAG_NAME, "h3")` → `Catch NoSuchElementException` | A NoSuchElementException is raised, confirming the driver's context is correctly locked inside the iFrame and cannot see the main document's elements. | High |
| TC_IF_04 | `test_invalid_frame_access_sad_path_tc4` | Negative Testing - Sad Path | Attempt to switch to a frame using a completely fictitious frame ID and verify the appropriate exception is raised. | `Navigate to /iframe` → `driver.switch_to.frame("ghost_frame_99")` → `Catch NoSuchFrameException` | A NoSuchFrameException is raised, confirming the WebDriver correctly validates frame IDs and rejects invalid ones. | Medium |
| TC_IF_05 | `test_sibling_frame_isolation_sad_path_tc5` | Negative Testing - Sad Path | From inside "frame-left", attempt to jump directly to the sibling "frame-right" without returning to the parent context first. | `switch_to.frame("frame-top")` → `switch_to.frame("frame-left")` → `try switch_to.frame("frame-right")` → `Catch NoSuchFrameException` | A NoSuchFrameException is raised, confirming that direct sibling-to-sibling frame navigation is not allowed and requires returning to a parent context first. | Medium |

---

## Feature: Geolocation
> **File:** test_geolocation.py

| Test Case ID | Method Name | Technique | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority |
|---|---|---|---|---|---|---|
| TC_GEO_01 | `test_tc1_geolocation_reveal_coordinates` | EP - Happy Path | Click the "Where am I?" button with a mocked GPS location (Hanoi, Vietnam) and verify the latitude and longitude values are displayed as valid numbers. | `CDP: Emulation.setGeolocationOverride (lat:21.0285, long:105.8542)` → `Click .example button` → `Wait for #lat-value` and `#long-value` → `float(lat.text)` | Valid floating-point numbers for latitude and longitude are displayed on the page, confirming the geolocation feature works with the mocked coordinates. | High |
| TC_GEO_02 | `test_tc2_geolocation_map_link` | EP - Happy Path | After triggering geolocation, verify that a Google Maps link appears with the correct latitude value embedded in the URL. | `Click .example button` → `Wait for #map-link a` → `href = get_attribute("href")` → `assertIn("google", href)` → `assertIn(lat, href)` | A Google Maps link is generated containing the word "google" and the exact mocked latitude value, confirming the dynamic URL construction works correctly. | Medium |

---

## Feature: Horizontal Slider
> **File:** test_horizontal_slider.py

| Test Case ID | Method Name | Technique | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority |
|---|---|---|---|---|---|---|
| TC_HS_01 | `test_tc1_slider_increments_correctly` | EP - Happy Path | Click on the slider and press the right arrow key once, then verify the slider value has incremented by exactly 0.5. | `Navigate to /horizontal_slider` → `Click input[type='range']` → `send_keys(Keys.ARROW_RIGHT)` → `assertEqual(new_value, initial_value + 0.5)` | The slider value increases by exactly 0.5 after pressing the right arrow key once, confirming the step increment is correctly configured. | Medium |
| TC_HS_02 | `test_tc2_slider_boundary_min` | BVA - Sad Path | Press the left arrow key 15 times on the slider to push it past the minimum possible value and verify it does not go below 0. | `Click input[type='range']` → `send_keys(Keys.ARROW_LEFT) × 15` → `assertEqual(range.text, "0")` | The slider stops at 0 and does not go below the minimum boundary, regardless of how many times the left arrow is pressed. | Medium |

---

## Feature: Hovers
> **File:** test_hovers.py

| Test Case ID | Method Name | Technique | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority |
|---|---|---|---|---|---|---|
| TC_HV_01 | `test_tc1_hover_user1` | EP - Happy Path | Hover over the first user profile image and verify the hidden caption reveals the correct username "user1". | `Navigate to /hovers` → `find_elements(By.CLASS_NAME, "figure")[0]` → `ActionChains.move_to_element()` → `JS: caption style opacity=1` → `assertEqual(caption_header.text, "name: user1")` | The caption "name: user1" appears when hovering over the first profile image, confirming the hover reveal works. | Medium |
| TC_HV_02 | `test_tc2_hover_user2` | EP - Happy Path | Hover over the second user profile image and verify the caption reveals "user2". | `figures[1]` → `move_to_element()` → `JS force opacity` → `assertEqual(caption_header.text, "name: user2")` | The caption "name: user2" appears on hover over the second image, confirming each image maps to the correct user. | Medium |
| TC_HV_03 | `test_tc3_hover_user3` | EP - Happy Path | Hover over the third user profile image and verify the caption reveals "user3". | `figures[2]` → `move_to_element()` → `JS force opacity` → `assertEqual(caption_header.text, "name: user3")` | The caption "name: user3" appears on hover over the third image, completing the verification of all three profile figures. | Medium |

---

## Feature: Infinite Scroll
> **File:** test_infinite_scroll.py

| Test Case ID | Method Name | Technique | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority |
|---|---|---|---|---|---|---|
| TC_IS_01 | `test_tc1_initial_content_load` | EP - Happy Path | Load the infinite scroll page and verify at least one content block is present immediately without any scrolling. | `Navigate to /infinite_scroll` → `Wait for EC.presence_of_element_located(By.CLASS_NAME, "jscroll-added")` → `assertGreaterEqual(count, 1)` | At least one paragraph content block is visible on the initial page load, confirming the page's default content renders correctly. | Medium |
| TC_IS_02 | `test_tc2_scroll_loads_more_content` | EP - Robustness | Scroll to the bottom of the page three times and verify that new content is appended each time, confirming the infinite scroll mechanism is active. | `get_paragraph_count() before` → `Loop 3×: execute_script("window.scrollTo(0, document.body.scrollHeight)")` → `time.sleep(1.5)` → `assertGreater(final_count, initial_count)` | The total number of content blocks increases after scrolling, confirming new content is dynamically loaded via AJAX as the user scrolls down. | High |

---

## Feature: Number Inputs
> **File:** test_inputs.py

| Test Case ID | Method Name | Technique | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority |
|---|---|---|---|---|---|---|
| TC_NI_01 | `test_tc1_valid_number_input` | EP - Happy Path | Type valid positive and negative integers into the number input field and verify the values are accepted and stored correctly. | `Navigate to /inputs` → `send_keys("500")` → `assertEqual(value, "500")` → `clear()` → `send_keys("-35")` → `assertEqual(value, "-35")` | Both "500" and "-35" are accepted by the number field and their values are correctly reflected in the input element. | Medium |
| TC_NI_02 | `test_tc2_arrow_up_increment` | EP - Happy Path | Type a starting value of 10, then press the up arrow key and verify the value increments by exactly 1. | `send_keys("10")` → `send_keys(Keys.ARROW_UP)` → `assertEqual(value, "11")` | The value increments from 10 to 11 after one up-arrow press, confirming the step increment is correctly set to 1. | Medium |
| TC_NI_03 | `test_tc3_arrow_down_decrement` | EP - Happy Path | Type a starting value of 10, then press the down arrow key and verify the value decrements by exactly 1. | `send_keys("10")` → `send_keys(Keys.ARROW_DOWN)` → `assertEqual(value, "9")` | The value decrements from 10 to 9 after one down-arrow press, confirming the decrement step is correctly set to 1. | Medium |
| TC_NI_04 | `test_tc4_invalid_text_input` | Negative Testing - Sad Path | Type alphabetical letters into a number-only input field and verify the field correctly rejects non-numeric input. | `send_keys("abc")` → `assertEqual(input.get_attribute("value"), "")` | The number input field ignores all alphabetical characters, leaving the value empty, confirming the browser-level type validation is working. | High |

---

## Feature: JavaScript Error Page
> **File:** test_javascript_error.py

| Test Case ID | Method Name | Technique | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority |
|---|---|---|---|---|---|---|
| TC_JSE_01 | `test_javascript_error_page_loads_tc1` | EP - Happy Path | Navigate to the JavaScript error page and verify the informational paragraph is visible despite the JS error firing on load. | `Navigate to /javascript_error` → `Wait for EC.presence_of_element_located(By.TAG_NAME, "p")` → `assertIn("JavaScript error", content.text)` | The page loads and the content paragraph containing "JavaScript error" is visible, confirming the page renders despite the JS error in the onload handler. | Medium |
| TC_JSE_02 | `test_javascript_error_console_log_tc2` | EP - Robustness | After loading the page, use JavaScript execution to confirm the known broken property access returns "undefined" and the error-triggering function exists in scope. | `execute_script("return typeof document.propertyThatDoesNotExist")` → `assertEqual(result, "undefined")` → `execute_script("return typeof window.loadError")` → `assertEqual(fn_type, "function")` | The broken property is correctly identified as "undefined" and the `loadError` function is confirmed to exist in the page's global scope. | Medium |
| TC_JSE_03 | `test_javascript_error_no_heading_tc3` | Negative Testing - Structural | Confirm that this specific page intentionally has no `<h3>` heading element, distinguishing it from other pages in the suite. | `Navigate to /javascript_error` → `find_elements(By.TAG_NAME, "h3")` → `assertEqual(len(h3_elements), 0)` | No `<h3>` elements are found, confirming the page structure is a bare `<p>` inside `<body>` without the standard heading wrapper. | Low |
| TC_JSE_04 | `test_javascript_error_page_title_tc4` | EP - Edge Case | Verify the browser tab title of the JavaScript error page is the correct, unique title rather than the generic site title. | `Navigate to /javascript_error` → `driver.title` → `assertIn("JavaScript error", title)` | The page title contains "JavaScript error", confirming the browser is on the correct page and not on the generic "The Internet" homepage. | Low |

---

## Feature: jQuery UI Menus
> **File:** test_jquery_ui_menus.py

| Test Case ID | Method Name | Technique | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority |
|---|---|---|---|---|---|---|
| TC_JQM_01 | `test_jquery_menu_hover_pdf_tc1` | EP - Happy Path | Expand the nested "Enabled → Downloads" menu hierarchy and verify the PDF download link is accessible with a correct href. | `Navigate to /jqueryui/menu` → `JS: force show Enabled submenu` → `JS: force show Downloads submenu` → `find_element(By.LINK_TEXT, "PDF")` → `assertIn("pdf", pdf_href.lower())` | The PDF link is found in the nested submenu and its href attribute contains "pdf", confirming the multi-level menu hierarchy is accessible. | High |
| TC_JQM_02 | `test_jquery_menu_hover_excel_tc2` | EP - Happy Path | Expand the "Enabled → Downloads" menu and verify the Excel download link is accessible with an "xls" href. | `Navigate to /jqueryui/menu` → `JS: force show Enabled submenu` → `JS: force show Downloads submenu` → `find_element(By.LINK_TEXT, "Excel")` → `assertIn("xls", excel_href.lower())` | The Excel link is found in the nested submenu and its href contains "xls", confirming all three nested download links are correctly wired. | Medium |
| TC_JQM_03 | `test_jquery_menu_disabled_not_clickable_tc3` | Negative Testing - Sad Path | Verify that clicking the "Disabled" top-level menu item does not navigate the user away from the current page. | `find_element(XPath //li[contains(@class,'ui-state-disabled')]/a)` → `assertIn("ui-state-disabled", classes)` → `disabled_item.click()` → `assertEqual(url_after_base, url_before_base)` | The URL remains unchanged after clicking the disabled item, confirming the jQuery UI disabled state correctly prevents navigation. | High |
| TC_JQM_04 | `test_jquery_menu_disabled_no_submenu_tc4` | Negative Testing - Sad Path | Confirm the "Disabled" menu item has no visible or accessible sub-menus hidden beneath it. | `find_element(XPath //li[contains(@class,'ui-state-disabled')])` → `disabled_li.find_elements(By.TAG_NAME, "ul")` → `For each ul: assertFalse(is_displayed())` | Any child `<ul>` elements within the disabled menu item are confirmed to be hidden and not displayed to the user. | Medium |

---

## Feature: JavaScript Alerts
> **File:** test_js_alerts.py

| Test Case ID | Method Name | Technique | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority |
|---|---|---|---|---|---|---|
| TC_JSA_01 | `test_tc1_accept_js_alert` | EP - Happy Path | Click the "JS Alert" button, verify the alert text, accept it, and confirm the result message updates correctly. | `Navigate to /javascript_alerts` → `Click button[onclick='jsAlert()']` → `Wait for EC.alert_is_present()` → `assertEqual(alert.text, "I am a JS Alert")` → `alert.accept()` → `assertEqual(result, "You successfully clicked an alert")` | The JS Alert shows the correct text, is dismissed successfully, and the page displays "You successfully clicked an alert". | High |
| TC_JSA_02 | `test_tc2_accept_js_confirm` | EP - Happy Path | Click the "JS Confirm" button, accept the confirmation dialog, and verify the result message shows "Ok" was clicked. | `Click button[onclick='jsConfirm()']` → `alert.accept()` → `assertEqual(result, "You clicked: Ok")` | After accepting the confirmation dialog, the result message "You clicked: Ok" is displayed, confirming the accept action is registered. | High |
| TC_JSA_03 | `test_tc3_dismiss_js_confirm` | Negative Testing - Sad Path | Click the "JS Confirm" button, dismiss (cancel) the dialog, and verify the result message shows "Cancel" was clicked. | `Click button[onclick='jsConfirm()']` → `alert.dismiss()` → `assertEqual(result, "You clicked: Cancel")` | After dismissing the confirmation dialog, the result message "You clicked: Cancel" is displayed, confirming the cancel action is correctly handled. | High |

---

## Feature: Key Presses
> **File:** test_key_presses.py

| Test Case ID | Method Name | Technique | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority |
|---|---|---|---|---|---|---|
| TC_KP_01 | `test_tc1_special_keyboard_keys` | EP - Happy Path | Press a series of special non-alphanumeric keys (Space, Enter, Tab, Escape, Backspace, Alt) and verify the page correctly identifies and displays each one. | `Navigate to /key_presses` → `ActionChains.send_keys(Keys.SPACE)` ... `Keys.ALT` → `For each: assertEqual(result, "You entered: {KEYNAME}")` | Each special key is correctly identified by name (e.g., "SPACE", "ENTER", "TAB") and displayed in the result section. | Medium |
| TC_KP_02 | `test_tc2_alphanumeric_keyboard_keys` | EP - Happy Path | Press basic printable characters (a, Z, 7, @) and verify the page echoes back the correct representation for each. | `ActionChains.send_keys("a")` → `assertEqual("You entered: A")` → `send_keys("Z")` → `assertEqual("You entered: Z")` → `send_keys("7")` → `assertEqual("You entered: 7")` | Alphanumeric keys are correctly echoed back in uppercase format; special symbols like "@" are echoed with their ASCII name. | Medium |

---

## Feature: Large & Deep DOM
> **File:** test_large_deep_dom.py

| Test Case ID | Method Name | Technique | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority |
|---|---|---|---|---|---|---|
| TC_LDD_01 | `test_large_dom_deep_sibling_tc1` | EP - Happy Path | Navigate to the large DOM page and locate a deeply nested sibling element by its exact ID, verifying the correct text content. | `Navigate to /large` → `find_element(By.ID, "sibling-2.2")` → `assertIn("2.2", text)` | The element with ID "sibling-2.2" is found and contains the text "2.2", confirming deep DOM traversal works at scale. | Medium |
| TC_LDD_02 | `test_large_dom_boundary_cell_tc2` | BVA - Happy Path | Use JavaScript to discover all sibling elements, sort them numerically, and verify the highest-indexed (BVA-max) boundary element exists with content. | `execute_script: Array.from(document.querySelectorAll('[id^="sibling-"]'))` → `Sort numerically` → `find_element(By.ID, boundary_id)` → `assertTrue(len(text) > 0)` | The boundary element at the largest sibling index is found and has non-empty text, confirming the DOM is fully rendered even at its deepest point. | Medium |
| TC_LDD_03 | `test_large_dom_invalid_id_sad_path_tc3` | Negative Testing - Sad Path | Attempt to locate a completely non-existent element ID in the large DOM and verify a timeout is raised gracefully. | `WebDriverWait(driver, 2).until(EC.presence_of_element_located(By.ID, "large-999-999"))` → `Catch TimeoutException` | A TimeoutException is raised, confirming the element does not exist and the test framework handles the absence gracefully. | Low |
| TC_LDD_04 | `test_large_dom_invalid_xpath_sad_path_tc4` | Negative Testing - Sad Path | Attempt to locate a non-existent element using an invalid XPath expression and verify the timeout is raised correctly. | `WebDriverWait(driver, 2).until(EC.presence_of_element_located(By.XPATH, "//div[@id='sibling-999.999']"))` → `Catch TimeoutException` | A TimeoutException is raised, confirming the XPath query correctly returns no results for the non-existent element. | Low |

---

## Feature: Multiple Windows
> **File:** test_multiple_windows.py

| Test Case ID | Method Name | Technique | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority |
|---|---|---|---|---|---|---|
| TC_MW_01 | `test_multiple_windows_switch_happy_path_tc1` | EP - Happy Path | Click a link that opens a new browser tab, switch the driver's context to the new tab, verify its content, close it, and return to the original tab. | `Navigate to /windows` → `Click "Click Here"` → `Wait for EC.number_of_windows_to_be(2)` → `switch_to.window(new_handle)` → `assertEqual(h3.text, "New Window")` → `close()` → `switch_to.window(original)` | The new window contains the heading "New Window". After closing it and switching back, the original window is still accessible and functional. | High |
| TC_MW_02 | `test_multiple_windows_isolation_sad_path_tc2` | Negative Testing - Sad Path | Open a new window but do NOT switch context, then attempt to read content from the new window without switching and verify the driver cannot see it. | `Click "Click Here"` → `Wait for 2 windows` → `try find_element(XPath //h3[text()='New Window'])` → `Catch NoSuchElementException` | A NoSuchElementException is raised, confirming the driver's context is strictly isolated to its current window handle. | High |
| TC_MW_03 | `test_invalid_window_handle_sad_path_tc3` | Negative Testing - Sad Path | Attempt to switch the driver to a completely fictitious window handle string and verify the correct exception is raised. | `driver.switch_to.window("ghost_tab_999")` → `Catch NoSuchWindowException` | A NoSuchWindowException is raised, confirming the WebDriver validates window handles and rejects invalid ones. | Medium |

---

## Feature: Nested Frames
> **File:** test_nested_frames.py

| Test Case ID | Method Name | Technique | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority |
|---|---|---|---|---|---|---|
| TC_NF_01 | `test_nested_frames_top_traversal_tc1` | EP - Happy Path | Traverse all three sibling frames within the top frame (LEFT, MIDDLE, RIGHT) sequentially and verify each contains the correct text content. | `Navigate to /nested_frames` → `switch_to.frame("frame-top")` → `switch_to.frame("frame-left")` → `assertEqual(body.text, "LEFT")` → `switch_to.parent_frame()` → `switch_to.frame("frame-middle")` → `assertEqual(content.text, "MIDDLE")` → ... RIGHT | Each of the three child frames (LEFT, MIDDLE, RIGHT) is accessed in order and contains the correct single-word text label. | High |
| TC_NF_02 | `test_nested_frames_bottom_traversal_tc2` | EP - Happy Path | Navigate from the root context directly into the bottom frame and verify it contains the text "BOTTOM". | `switch_to.default_content()` → `switch_to.frame("frame-bottom")` → `assertEqual(body.text, "BOTTOM")` | The bottom frame is accessible directly from the root context and contains the text "BOTTOM". | Medium |
| TC_NF_03 | `test_nested_frames_sibling_isolation_tc3` | Negative Testing - Sad Path | From inside "frame-left", attempt a direct jump to the sibling "frame-right" and verify this illegal navigation is blocked. | `switch_to.frame("frame-top")` → `switch_to.frame("frame-left")` → `try switch_to.frame("frame-right")` → `Catch NoSuchFrameException` | A NoSuchFrameException is raised, confirming you cannot jump directly between sibling frames without first returning to the parent context. | Medium |

---

## Feature: Notification Messages
> **File:** test_notification_messages.py

| Test Case ID | Method Name | Technique | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority |
|---|---|---|---|---|---|---|
| TC_NM_01 | `test_notification_single_click_ep_tc1` | EP - Happy Path | Click the notification trigger link once and verify the flash message displayed is one of the two known valid server responses. | `Navigate to /notification_message` → `Click "Click here"` → `Wait for #flash` → `assertIn(flash_text, VALID_MESSAGES)` | The flash message is one of the two recognized responses ("Action successful" or "Action unsuccessful, please try again"), confirming the notification system is functional. | High |
| TC_NM_02 | `test_notification_multi_click_ep_tc2` | EP - Robustness | Click the notification trigger link 5 times in sequence and verify each click produces a valid flash message response. | `Loop 5×: Navigate to /notification_message` → `Click "Click here"` → `assertIn(flash_text, VALID_MESSAGES)` | All 5 clicks produce a valid flash message, confirming the notification system is stable and consistent across repeated interactions. | Medium |
| TC_NM_03 | `test_notification_no_unexpected_message_tc3` | Negative Testing - Sad Path | Click the notification link and verify the flash message is never empty and is always one of the two known server-defined messages. | `Click "Click here"` → `assertTrue(len(flash_text) > 0)` → `assertIn(flash_text, VALID_MESSAGES)` | The flash message is non-empty and matches one of the two known valid messages, confirming no unexpected or unknown responses are returned. | Medium |
| TC_NM_04 | `test_notification_direct_render_robustness_tc4` | EP - Robustness | Follow the full click-to-redirect flow and confirm the final rendered URL is the expected notification-rendered endpoint with a valid flash message. | `Navigate to /notification_message` → `Click "Click here"` → `Wait for EC.url_contains("notification_message_rendered")` → `assertIn(flash_text, VALID_MESSAGES)` | After the click and redirect, the URL contains "notification_message_rendered" and the flash message on the destination page is valid. | Medium |


---

## Feature: Redirect Link
> **File:** test_redirect_link.py

| Test Case ID | Method Name | Technique | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority |
|---|---|---|---|---|---|---|
| TC_RL_01 | `test_redirect_link_url_change_tc1` | EP - Happy Path | Click the redirect link on the redirector page and verify the browser URL changes to the expected destination page. | `Navigate to /redirector` → `Click CSS a[href='redirect']` → `Wait for EC.url_contains("status_codes")` → `assertNotEqual(url_before, url_after)` → `assertEqual(url_after, /status_codes)` | The URL changes from `/redirector` to the expected `/status_codes` destination, confirming the redirect mechanism is functional. | High |
| TC_RL_02 | `test_redirect_link_destination_content_tc2` | EP - Happy Path | Follow the redirect and verify the destination page displays the correct "Status Codes" heading. | `Navigate to /redirector` → `Click redirect link` → `Wait for h3` → `assertIn("Status Codes", heading.text)` | After the redirect, the page heading contains "Status Codes", confirming the user lands on the correct destination page with the right content. | High |
| TC_RL_03 | `test_redirect_invalid_endpoint_tc3` | Negative Testing - Sad Path | Navigate directly to an invalid redirect endpoint URL and verify the Status Codes page is not accidentally displayed. | `Navigate to /redirect/nonexistent_page_404` → `assertNotIn("Status Codes", body_text)` | The "Status Codes" page content is absent, confirming the invalid redirect endpoint correctly does not serve the expected destination page. | Medium |
| TC_RL_04 | `test_redirect_link_absent_on_wrong_page_tc4` | Negative Testing - Sad Path | Navigate to the redirect destination page directly and verify the "redirect" trigger link is not present on that page. | `Navigate to /status_codes` → `WebDriverWait(driver, 2).until(presence_of(CSS a[href='redirect']))` → `Catch TimeoutException` | A TimeoutException is raised, confirming the redirect trigger link is exclusive to the `/redirector` page and not present on the destination. | Low |

---

## Feature: Secure File Download
> **File:** test_secure_file_download.py

| Test Case ID | Method Name | Technique | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority |
|---|---|---|---|---|---|---|
| TC_SFD_01 | `test_secure_download_auth_happy_path_tc1` | EP - Happy Path | Access the secure file download area using valid credentials embedded in the URL and verify that file download links are accessible. | `Navigate to https://admin:admin@.../download_secure` → `Wait for EC.presence_of_element_located(By.CSS_SELECTOR, ".example a")` → `assertTrue(first_link.is_displayed())` | After authenticating, at least one file download link is visible and accessible in the secure area. | Critical |
| TC_SFD_02 | `test_secure_download_unauth_sad_path_tc2` | Security Testing - Sad Path | Attempt to access the secure file download page without providing any credentials and verify the file links are not accessible. | `Navigate to https://the-internet.herokuapp.com/download_secure` (no credentials)` → `WebDriverWait(driver, 3).until(presence_of(".example a"))` → `Catch TimeoutException` | The file listing is not displayed when no credentials are provided, confirming the download area is protected and inaccessible without authentication. | Critical |

---

## Feature: Shadow DOM
> **File:** test_shadow_dom.py

| Test Case ID | Method Name | Technique | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority |
|---|---|---|---|---|---|---|
| TC_SD_01 | `test_shadow_dom_access_via_shadow_root_tc1` | EP - Happy Path | Use Selenium 4's native Shadow Root API to access the content inside a custom web component and verify the text is readable. | `Navigate to /shadowdom` → `find_element(By.CSS_SELECTOR, "my-paragraph")` → `.shadow_root` → `find_element(By.CSS_SELECTOR, "p")` → `assertTrue(len(text) > 0)` | The inner `<p>` text inside the Shadow DOM is successfully accessed via the Selenium 4 `.shadow_root` property and returns non-empty content. | High |
| TC_SD_02 | `test_shadow_dom_access_via_js_tc2` | EP - Happy Path | Pierce the Shadow DOM boundary using a JavaScript injection and verify the content can be retrieved via script execution. | `execute_script: host.shadowRoot.querySelector('p').textContent` → `assertIsNotNone(text)` → `assertTrue(len(text) > 0)` | The JavaScript injection successfully pierces the Shadow DOM boundary and returns non-empty text content from inside the web component. | High |
| TC_SD_03 | `test_shadow_dom_xpath_cannot_pierce_tc3` | Negative Testing - Sad Path | Attempt to locate the Shadow DOM's inner elements using a standard global XPath query and verify it is correctly blocked by the shadow boundary. | `WebDriverWait(driver, 2).until(presence_of(By.XPATH, "//my-paragraph//p[contains(text(),'shadow')]"))` → `Catch TimeoutException or NoSuchElementException` | Standard XPath cannot cross the Shadow DOM boundary, and a timeout or not-found exception is correctly raised, confirming the encapsulation is working. | Medium |

---

## Feature: Shifting Content
> **File:** test_shifting_content.py

| Test Case ID | Method Name | Technique | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority |
|---|---|---|---|---|---|---|
| TC_SC_01 | `test_tc1_menu_renders_successfully_despite_shifting` | EP - Robustness | Load the shifting content menu page and verify that at least 5 menu items render correctly and that the first item is visible and clickable. | `Navigate to /shifting_content/menu` → `Wait for EC.presence_of_all_elements_located(By.CSS_SELECTOR, "ul li a")` → `assertTrue(len(menu_items) >= 5)` → `assertTrue(first_item.is_displayed() and is_enabled())` | At least 5 shifting menu items are present, and the first item is both visible and interactable, confirming the shifting content page renders reliably. | Medium |

---

## Feature: Slow Resources
> **File:** test_slow_resources.py

| Test Case ID | Method Name | Technique | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority |
|---|---|---|---|---|---|---|
| TC_SR_01 | `test_slow_resources_full_load_tc1` | EP - Happy Path | Navigate to the intentionally slow-loading page and verify it fully loads within a generous 30-second window. | `Navigate to /slow` → `WebDriverWait(driver, 30).until(EC.visibility_of_element_located(By.TAG_NAME, "h3"))` → `assertTrue(heading.is_displayed())` | The page heading is visible within 30 seconds, confirming the slow-loading page eventually completes its full load cycle. | High |
| TC_SR_02 | `test_slow_resources_perf_entry_exists_tc2` | EP - Robustness | After loading the slow page, query the browser's Performance API to verify a navigation timing entry exists with a non-zero duration. | `WebDriverWait(driver, 30)` → `execute_script("return window.performance.getEntriesByType('navigation')")` → `assertGreater(len(entries), 0)` → `assertGreater(duration, 0)` | At least one navigation performance entry exists with a duration greater than 0ms, confirming a real network round-trip occurred and is being measured. | Medium |
| TC_SR_03 | `test_slow_resources_page_structure_tc3` | EP - Happy Path | After the slow page loads, verify the current URL contains "/slow" and the page heading is not empty. | `WebDriverWait(driver, 30)` → `assertIn("/slow", driver.current_url)` → `assertTrue(len(heading_text) > 0)` | The URL contains "/slow" and the page heading is non-empty, confirming the correct page loaded with valid content. | Medium |

---

## Feature: Sortable Data Tables
> **File:** test_sortable_data_tables.py

| Test Case ID | Method Name | Technique | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority |
|---|---|---|---|---|---|---|
| TC_SDT_01 | `test_sortable_tables_sort_lastname_asc_tc1` | EP - Happy Path | Click the "Last Name" column header once and verify the column data is sorted in ascending alphabetical order. | `Navigate to /tables` → `Click XPath //table[@id='table1']//th[span[text()='Last Name']]` → `_get_column_values("table1", 1)` → `assertEqual(actual, sorted(actual))` | The "Last Name" column is sorted in ascending (A-Z) alphabetical order after a single click on the column header. | High |
| TC_SDT_02 | `test_sortable_tables_sort_lastname_desc_tc2` | EP - Happy Path | Click the "Last Name" column header twice and verify the data reverses to a descending (Z-A) sort order. | `Click header twice` → `_get_column_values("table1", 1)` → `assertEqual(actual, sorted(actual, reverse=True))` | The "Last Name" column is sorted in descending (Z-A) order after the second click on the header, confirming the toggle sort works. | High |
| TC_SDT_03 | `test_sortable_tables_unsortable_column_tc3` | BVA - Happy Path | Click the "Email" column header in Table 2 and verify it is also sortable, returning data in alphabetical order. | `Click XPath //table[@id='table2']//th[span[text()='Email']]` → `_get_column_values("table2", 3)` → `assertEqual(values_after, sorted(values_after))` | The Email column in Table 2 is successfully sorted alphabetically after clicking the header, confirming all columns in both tables are sortable. | Medium |
| TC_SDT_04 | `test_sortable_tables_out_of_bounds_column_tc4` | Negative Testing - Sad Path | Attempt to extract data from a non-existent column index (99) and verify the system returns an empty result gracefully. | `_get_column_values("table1", col_index=99)` → `assertEqual(values, [])` | An empty list is returned for the out-of-bounds column index, confirming the helper method handles invalid column requests gracefully without crashing. | Low |

---

## Feature: HTTP Status Codes
> **File:** test_status_codes.py

| Test Case ID | Method Name | Technique | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority |
|---|---|---|---|---|---|---|
| TC_STC_01 | `test_tc1_status_code_200_ok` | EP - Happy Path | Click the "200" link and verify the destination page confirms a successful HTTP 200 OK response. | `Navigate to /status_codes` → `Click link "200"` → `Wait for .example p` → `assertIn("This page returned a 200 status code.", status_text)` | The page confirms receipt of a 200 OK status code, indicating a fully successful response. | High |
| TC_STC_02 | `test_tc2_status_code_301_moved` | EP - Happy Path | Click the "301" link and verify the destination page confirms a 301 Moved Permanently redirect response. | `Navigate to /status_codes` → `Click link "301"` → `assertIn("This page returned a 301 status code.", status_text)` | The page confirms receipt of a 301 status code, indicating the resource has been permanently moved. | Medium |
| TC_STC_03 | `test_tc3_status_code_404_not_found` | Negative Testing - Sad Path | Click the "404" link and verify the destination page correctly identifies the Not Found error response. | `Navigate to /status_codes` → `Click link "404"` → `assertIn("This page returned a 404 status code.", status_text)` | The page confirms receipt of a 404 status code, indicating the requested resource was not found on the server. | High |
| TC_STC_04 | `test_tc4_status_code_500_server_error` | Negative Testing - Sad Path | Click the "500" link and verify the destination page correctly identifies the Internal Server Error response. | `Navigate to /status_codes` → `Click link "500"` → `assertIn("This page returned a 500 status code.", status_text)` | The page confirms receipt of a 500 status code, indicating a server-side error, with the application handling it gracefully. | High |

---

## Feature: Typos (A/B Content Bug Detection)
> **File:** test_typos.py

| Test Case ID | Method Name | Technique | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority |
|---|---|---|---|---|---|---|
| TC_TY_01 | `test_typos_refresh_until_correct_tc1` | EP - Happy Path | Refresh the page up to 10 times until the grammatically correct version of the sentence ("won't") appears, then stop. | `Loop up to 10×: Navigate to /typos` → `_get_second_paragraph()` → `If CORRECT_TEXT in text: break` → `assertTrue(found_correct)` | The correct version of the sentence (containing "won't") is found within 10 page loads, confirming the page does serve the correct content variant. | Medium |
| TC_TY_02 | `test_typos_detect_known_typo_tc2` | Negative Testing - Bug Detection | Load the page and scan for the known A/B typo variant ("won,t") within 10 attempts, logging it as a content defect if found. | `Loop up to 10×: Navigate to /typos` → `_get_second_paragraph()` → `If TYPO_TEXT in text: found_typo = True; break` → `Log result` | Either the known typo ("won,t") is detected and logged as an A/B content defect, or the correct variant is observed. Either outcome is a pass — the goal is detection and documentation. | Medium |
| TC_TY_03 | `test_typos_page_structure_robustness_tc3` | EP - Robustness | Verify the page always renders exactly 2 paragraphs regardless of which A/B content variant is served. | `Navigate to /typos` → `find_elements(By.CSS_SELECTOR, "div.example p")` → `assertEqual(len(paragraphs), 2)` → `assertIn(second_text, known_variants)` | The page always has exactly 2 paragraphs, and the second paragraph is always one of the two known A/B variants, confirming structural consistency. | Medium |

---

## Feature: WYSIWYG Editor (TinyMCE)
> **File:** test_wysiwyg_editor.py

| Test Case ID | Method Name | Technique | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority |
|---|---|---|---|---|---|---|
| TC_WYS_01 | `test_wysiwyg_js_injection_happy_path_tc1` | EP - Happy Path | Switch into the TinyMCE iFrame, inject custom text into the editor body using JavaScript, and verify the content is correctly written. | `Navigate to /tinymce` → `Wait for EC.frame_to_be_available_and_switch_to_it(By.ID, "mce_0_ifr")` → `execute_script: editor_body.innerHTML = "<p>INJECT_TEXT</p>"` → `assertIn(INJECT_TEXT, innerHTML)` | The injected text is confirmed present in the TinyMCE editor's HTML body, proving that JavaScript-level content injection bypasses the read-only constraint. | High |
| TC_WYS_02 | `test_wysiwyg_readonly_alert_sad_path_tc2` | Negative Testing - Robustness | Load the TinyMCE editor page and check whether a read-only API-limit warning overlay appears, handling either outcome as a valid test result. | `Navigate to /tinymce` → `WebDriverWait(driver, 5).until(presence_of(".tox-notification--warning"))` → `assertTrue(warning_overlay.is_displayed())` OR `Catch TimeoutException` | If the read-only overlay is present, it is correctly identified and verified. If absent (TinyMCE loaded normally), the test also passes — both are valid states for this demo app. | Medium |
| TC_WYS_03 | `test_wysiwyg_toolbar_visibility_happy_path_tc3` | EP - Happy Path | Load the WYSIWYG editor page and verify that the Bold and Italic toolbar buttons are visible in the main document context. | `Navigate to /tinymce` → `Wait for .tox-toolbar__primary` → `find_element(XPath //button[@aria-label='Bold'])` → `assertTrue(bold_btn.is_displayed())` → same for `Italic` | Both the Bold and Italic toolbar buttons are visible and rendered in the TinyMCE toolbar, confirming the editor UI loaded correctly. | High |
| TC_WYS_04 | `test_wysiwyg_context_isolation_sad_path_tc4` | Negative Testing - Sad Path | Switch into the TinyMCE iFrame and then attempt to find the main-document toolbar buttons, verifying they are invisible from inside the frame context. | `frame_to_be_available_and_switch_to_it(By.ID, "mce_0_ifr")` → `try find_element(XPath //button[@aria-label='Bold'])` → `Catch NoSuchElementException` | A NoSuchElementException is raised because toolbar buttons live in the main document, not inside the iFrame, confirming correct context isolation. | Medium |

---

## Summary

| # | Feature | File | Total TCs | Critical | High | Medium | Low |
|---|---|---|---|---|---|---|---|
| 1 | A/B Testing | test_ab_testing.py | 4 | 0 | 2 | 2 | 0 |
| 2 | Add/Remove Elements | test_add_remove_elements.py | 4 | 0 | 2 | 2 | 0 |
| 3 | Basic Authentication | test_basic_auth.py | 9 | 1 | 3 | 5 | 0 |
| 4 | Broken Images | test_broken_images.py | 3 | 0 | 1 | 2 | 0 |
| 5 | Challenging DOM | test_challenging_dom.py | 8 | 0 | 3 | 4 | 1 |
| 6 | Checkboxes | test_checkbox.py | 4 | 0 | 3 | 1 | 0 |
| 7 | Context Menu | test_context_menu.py | 3 | 0 | 1 | 2 | 0 |
| 8 | Digest Authentication | test_digest_auth.py | 4 | 3 | 1 | 0 | 0 |
| 9 | Disappearing Elements | test_disappearing_elements.py | 2 | 0 | 1 | 1 | 0 |
| 10 | Drag and Drop | test_drag_and_drop.py | 2 | 0 | 1 | 1 | 0 |
| 11 | Dropdown | test_dropdown.py | 4 | 0 | 3 | 1 | 0 |
| 12 | Dynamic Content | test_dynamic_content.py | 3 | 0 | 0 | 2 | 1 |
| 13 | Dynamic Controls | test_dynamic_controls.py | 4 | 0 | 4 | 0 | 0 |
| 14 | Dynamic Loading | test_dynamic_loading.py | 5 | 2 | 0 | 3 | 0 |
| 15 | Entry Ad (Modal) | test_entry_ad.py | 3 | 0 | 2 | 1 | 0 |
| 16 | Exit Intent | test_exit_intent.py | 4 | 0 | 2 | 2 | 0 |
| 17 | File Download | test_file_download.py | 1 | 0 | 1 | 0 | 0 |
| 18 | File Upload | test_file_upload.py | 2 | 0 | 2 | 0 | 0 |
| 19 | Floating Menu | test_floating_menu.py | 3 | 0 | 1 | 2 | 0 |
| 20 | Forgot Password | test_forgot_password.py | 3 | 0 | 0 | 2 | 1 |
| 21 | Form Authentication | test_form_authentication.py | 10 | 4 | 3 | 3 | 0 |
| 22 | iFrame & Frames | test_frame.py | 5 | 0 | 3 | 2 | 0 |
| 23 | Geolocation | test_geolocation.py | 2 | 0 | 1 | 1 | 0 |
| 24 | Horizontal Slider | test_horizontal_slider.py | 2 | 0 | 0 | 2 | 0 |
| 25 | Hovers | test_hovers.py | 3 | 0 | 0 | 3 | 0 |
| 26 | Infinite Scroll | test_infinite_scroll.py | 2 | 0 | 1 | 1 | 0 |
| 27 | Number Inputs | test_inputs.py | 4 | 0 | 1 | 3 | 0 |
| 28 | JavaScript Error Page | test_javascript_error.py | 4 | 0 | 0 | 2 | 2 |
| 29 | jQuery UI Menus | test_jquery_ui_menus.py | 4 | 0 | 2 | 2 | 0 |
| 30 | JavaScript Alerts | test_js_alerts.py | 3 | 0 | 3 | 0 | 0 |
| 31 | Key Presses | test_key_presses.py | 2 | 0 | 0 | 2 | 0 |
| 32 | Large & Deep DOM | test_large_deep_dom.py | 4 | 0 | 0 | 2 | 2 |
| 33 | Multiple Windows | test_multiple_windows.py | 3 | 0 | 2 | 1 | 0 |
| 34 | Nested Frames | test_nested_frames.py | 3 | 0 | 1 | 2 | 0 |
| 35 | Notification Messages | test_notification_messages.py | 4 | 0 | 1 | 3 | 0 |
| 36 | Redirect Link | test_redirect_link.py | 4 | 0 | 2 | 1 | 1 |
| 37 | Secure File Download | test_secure_file_download.py | 2 | 2 | 0 | 0 | 0 |
| 38 | Shadow DOM | test_shadow_dom.py | 3 | 0 | 2 | 1 | 0 |
| 39 | Shifting Content | test_shifting_content.py | 1 | 0 | 0 | 1 | 0 |
| 40 | Slow Resources | test_slow_resources.py | 3 | 0 | 1 | 2 | 0 |
| 41 | Sortable Data Tables | test_sortable_data_tables.py | 4 | 0 | 2 | 1 | 1 |
| 42 | HTTP Status Codes | test_status_codes.py | 4 | 0 | 3 | 1 | 0 |
| 43 | Typos (A/B Bug Detection) | test_typos.py | 3 | 0 | 0 | 3 | 0 |
| 44 | WYSIWYG Editor (TinyMCE) | test_wysiwyg_editor.py | 4 | 0 | 2 | 2 | 0 |
| | **TOTAL** | **44 files** | **128** | **12** | **57** | **52** | **9** |

---
*Generated by Senior QA Automation Architect · Reverse-Engineered from Source · 2026-05-07*
