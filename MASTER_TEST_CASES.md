# MASTER AUTOMATION TEST CASES

This document provides a comprehensive overview of the automated test cases implemented for the "The Internet" (Herokuapp) Selenium suite. Every test case is reverse-engineered from the active Python test scripts under the `tests/` directory.

---

## Feature: A/B Testing
Validates that the page header correctly reflects A/B variants or opt-out status.
> **File:** test_ab_testing.py

| Test Case ID | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority | Testing Technique |
| --- | --- | --- | --- | --- | --- |
| test_ab_testing_header_variation_tc1 | Happy Path: Header variation check | `get(BASE_URL)`, `visibility_of_element_located(By.TAG_NAME, "h3")` | Header text is in `VALID_HEADERS` list. | High | **EP** |
| test_ab_testing_paragraph_presence_tc2 | Happy Path: UI Info paragraph check | `get(BASE_URL)`, `visibility_of_element_located((By.XPATH, "//p[contains(text(),'Also known as...')]"))` | Informational paragraph is visible. | Medium | **EP** |
| test_ab_testing_optout_cookie_tc3 | Robustness: Opt-out cookie functionality | `add_cookie({'name': 'optimizelyOptOut', 'value': 'true'})`, `refresh()` | Header text becomes "No A/B Test". | High | **State Transition** |

---

## Feature: Add / Remove Elements
Tests the dynamic addition and removal of action buttons in the DOM.
> **File:** test_add_remove_elements.py

| Test Case ID | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority | Testing Technique |
| --- | --- | --- | --- | --- | --- |
| test_tc1_add_single_element | Happy Path: Add one element | Click `//button[text()='Add Element']` | One `added-manually` button appears. | High | **EP** |
| test_tc2_remove_single_element | Happy Path: Remove one element | Click `added-manually` button, wait for `staleness_of` | Zero `added-manually` buttons remain. | High | **State Transition** |
| test_tc3_add_multiple_elements | Happy Path: Stress dynamic addition | Loop 5 times: click 'Add Element' | Exactly 5 delete buttons are present. | Medium | **BVA** |
| test_tc4_remove_all_elements_dynamically | Happy Path: Full removal loop | Add 3 elements, loop 3 times: click 'Delete' | DOM is cleared of all added elements. | High | **BVA** |

---

## Feature: Basic Authentication
Verifies successful authentication via URL-embedded credentials.
> **File:** test_basic_auth.py

| Test Case ID | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority | Testing Technique |
| --- | --- | --- | --- | --- | --- |
| test_basic_auth_success | Happy Path: Successful credential login | `get('https://admin:admin@host/basic_auth')` | Page contains "Congratulations!". | Critical | **EP** |

---

## Feature: Broken Images
Detects broken image assets via HTTP status code verification.
> **File:** test_broken_images.py

| Test Case ID | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority | Testing Technique |
| --- | --- | --- | --- | --- | --- |
| test_tc1_verify_total_images_on_page | Happy Path: Layout audit | `find_elements(By.TAG_NAME, "img")` | At least 3 images are present. | Low | **BVA** |
| test_tc2_identify_broken_images | Happy Path: Broken asset detection | `requests.get(img_src)` for all images | Exactly 2 images return non-200 codes. | High | **EP** |
| test_tc3_identify_valid_images | Happy Path: Valid asset verification | `requests.get(img_src)` check for avatar | At least one image returns 200 OK. | Medium | **EP** |

---

## Feature: Challenging DOM
Tests interaction with dynamically generated elements and data extraction.
> **File:** test_challenging_dom.py

| Test Case ID | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority | Testing Technique |
| --- | --- | --- | --- | --- --- |
| test_dynamic_buttons_tc1 | Happy Path: Locate alert button | Click `.button.alert` (no ID used) | Button remains visible after DOM refresh. | High | **EP** |
| test_table_ep_mid_tc2 | Happy Path: Row 5 data extraction | Locate row 5 via XPath | Row contains valid EP data. | Medium | **EP** |
| test_table_bva_min_tc3 | Happy Path: Row 1 data extraction | Locate row 1 via XPath | Row contains valid BVA min data. | Medium | **BVA** |
| test_table_bva_max_tc4 | Happy Path: Row 10 data extraction | Locate row 10 via XPath | Row contains valid BVA max data. | Medium | **BVA** |
| test_table_negative_out_of_bounds_tc5 | Sad Path: Out of bounds check | Attempt to find row 11 (2s timeout) | `TimeoutException`/`NoSuchElementException` caught. | Low | **Negative Testing** |
| test_canvas_verification_tc6 | Happy Path: Canvas rendering | `presence_of_element_located((By.CSS_SELECTOR, "canvas#canvas"))` | Canvas is visible on UI. | Medium | **EP** |
| test_table_action_links_tc7 | Happy Path: Action link interaction | Click 'edit' and 'delete' in row 3 | URL hash updates to `#edit` and `#delete`. | High | **EP** |

---

## Feature: Checkboxes
Verifies boolean state management of HTML input elements.
> **File:** test_checkbox.py

| Test Case ID | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority | Testing Technique |
| --- | --- | --- | --- | --- | --- |
| test_tc1_default_state_validation | Happy Path: Default state audit | `is_selected()` on both checkboxes | CB1 is unchecked, CB2 is checked. | Medium | **BVA** |
| test_tc2_check_first_checkbox | Happy Path: Check action | Click CB1 if `not is_selected()` | `is_selected()` returns True. | High | **EP** |
| test_tc3_uncheck_second_checkbox | Happy Path: Uncheck action | Click CB2 if `is_selected()` | `is_selected()` returns False. | High | **EP** |
| test_tc4_toggle_both_checkboxes | Robustness: Toggle stress test | Sequential clicks on CB1 & CB2 | States flip correctly across multiple clicks. | Medium | **EP** |

---

## Feature: Context Menu
Validates JavaScript alert triggers on right-click actions.
> **File:** test_context_menu.py

| Test Case ID | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority | Testing Technique |
| --- | --- | --- | --- | --- | --- |
| test_tc1_context_menu_success | Happy Path: Trigger menu | `ActionChains.context_click(hot_spot)` | JS Alert "You selected a context menu" appears. | High | **State Transition** |
| test_tc2_left_click_ignores_menu | Sad Path: Invalid trigger check | `ActionChains.click(hot_spot)` | No alert appears (2s short-wait). | Medium | **Negative Testing** |

---

## Feature: Digest Authentication
Handles challenge-response authentication with URL encoding.
> **File:** test_digest_auth.py

| Test Case ID | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority | Testing Technique |
| --- | --- | --- | --- | --- | --- |
| test_digest_auth_happy_path_tc1 | Happy Path: Valid login | `get("https://admin:admin@host/digest_auth")` | "Congratulations!" message visible. | Critical | **EP** |
| test_digest_auth_invalid_creds_tc2 | Sad Path: Wrong password | `get("https://admin:wrong@host/digest_auth")` | Success message is absent from body. | High | **Negative Testing** |
| test_digest_auth_unauthorized_tc3 | Sad Path: No credentials | `get("https://host/digest_auth")` | Success message is absent from body. | High | **Negative Testing** |
| test_digest_auth_special_chars_tc4 | Robustness: URL encoding verification | `urllib.parse.quote("admin@123")` | '@' becomes '%40'; login rejected correctly. | Medium | **BVA** |

---

## Feature: Disappearing Elements
Tests for volatile DOM elements caused by A/B variation logic.
> **File:** test_disappearing_elements.py

| Test Case ID | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority | Testing Technique |
| --- | --- | --- | --- | --- | --- |
| test_tc1_verify_permanent_links | Happy Path: Static link audit | Find "Home", "About", "Contact Us", "Portfolio" | All 4 permanent links are present. | Medium | **EP** |
| test_tc2_gallery_appears_on_refresh | Happy Path: Volatile element detection | Refresh up to 5 times for "Gallery" link | "Gallery" appears and leads to 404 handler. | High | **BVA** |

---

## Feature: Drag and Drop
Simulates HTML5 drag and drop via JavaScript injection.
> **File:** test_drag_and_drop.py

| Test Case ID | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority | Testing Technique |
| --- | --- | --- | --- | --- | --- |
| test_tc1_drag_a_to_b | Happy Path: Swap blocks | Execute JS helper to drag A to B | Block A text is "B", Block B text is "A". | High | **State Transition** |
| test_tc2_drag_b_to_a | Happy Path: Reverse swap | Drag A to B, then B to A | Blocks revert to "A" and "B" respectively. | High | **State Transition** |

---

## Feature: Dropdown
Validates standard HTML Select element interactions.
> **File:** test_dropdown.py

| Test Case ID | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority | Testing Technique |
| --- | --- | --- | --- | --- | --- |
| test_tc1_default_placeholder | Happy Path: Placeholder audit | `dropdown.first_selected_option` | Text is "Please select an option"; disabled. | Low | **BVA** |
| test_tc2_select_option_1 | Happy Path: Select by index | `dropdown.select_by_index(1)` | Selected text is "Option 1". | High | **EP** |
| test_tc3_select_option_2 | Happy Path: Select by text | `dropdown.select_by_visible_text("Option 2")` | Selected text is "Option 2". | High | **EP** |
| test_tc4_switch_between_options | Happy Path: Selection override | Select "1", then select "2" | Final selection is "Option 2". | Medium | **State Transition** |

---

## Feature: Dynamic Content
Detects randomization of images and text blocks.
> **File:** test_dynamic_content.py

| Test Case ID | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority | Testing Technique |
| --- | --- | --- | --- | --- | --- |
| test_tc1_content_structure_intact | Happy Path: Layout verification | `find_elements(By.CSS_SELECTOR, ".row")` | Exactly 3 images and 3 text blocks render. | Medium | **BVA** |
| test_tc2_content_changes_on_refresh | Happy Path: Randomization check | Capture state, refresh, compare | At least some content changes after refresh. | High | **EP** |
| test_tc3_static_content_parameter | Happy Path: Static mode check | `get(url + "?with_content=static")`, refresh | First two rows remain identical on refresh. | Medium | **State Transition** |

---

## Feature: Dynamic Controls
Manages asynchronous element addition/removal and state toggling.
> **File:** test_dynamic_controls.py

| Test Case ID | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority | Testing Technique |
| --- | --- | --- | --- | --- | --- |
| test_tc1_checkbox_removal | Happy Path: Remove checkbox | Click "Remove", `wait.until(staleness_of)` | Message "It's gone!" appears; CB removed. | High | **State Transition** |
| test_tc2_checkbox_addition | Happy Path: Add checkbox | Click "Add", wait for presence | Message "It's back!" appears; CB present. | High | **State Transition** |
| test_tc3_input_enable | Happy Path: Enable input | Click "Enable", wait for clickable | Message "It's enabled!"; `is_enabled()` is True. | High | **State Transition** |
| test_tc4_input_disable | Happy Path: Disable input | Click "Disable", wait for condition | Message "It's disabled!"; `is_enabled()` is False. | High | **State Transition** |

---

## Feature: Dynamic Loading
Validates UX for elements becoming visible after AJAX or rendering delays.
> **File:** test_dynamic_loading.py

| Test Case ID | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority | Testing Technique |
| --- | --- | --- | --- | --- | --- |
| test_hidden_element_ep_tc1 | Happy Path: Hidden element (Ex 1) | Click Start, wait for loading invis | "Hello World!" becomes visible. | High | **EP** |
| test_rendered_element_ep_tc2 | Happy Path: Rendered element (Ex 2) | Click Start, wait for presence | "Hello World!" added to DOM and visible. | High | **EP** |
| test_double_click_sad_path_tc3 | Robustness: Double-click start | Rapidly click Start twice | Page recovers gracefully and shows content. | Medium | **BVA** |
| test_missing_element_sad_path_tc4 | Sad Path: Invalid selector | Wait for `button#wrong-id` | `TimeoutException` is correctly thrown. | Low | **Negative Testing** |
| test_short_timeout_bva_tc5 | Robustness: BVA timing check | Wait with 0.5s timeout | `TimeoutException` (loading takes >0.5s). | Medium | **BVA** |

---

## Feature: Entry Ad
Tests modal dismissal logic using cookies for session retention.
> **File:** test_entry_ad.py

| Test Case ID | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority | Testing Technique |
| --- | --- | --- | --- | --- | --- |
| test_tc1_close_entry_ad_modal | Happy Path: Basic dismissal | `execute_script("modal_close.click()")` | Modal ID='modal' becomes invisible. | High | **State Transition** |
| test_tc2_ad_does_not_reappear_on_refresh | Happy Path: Cookie retention | Dismiss ad, refresh | Modal does not reappear (3s short-wait). | High | **BVA** |
| test_tc3_ad_reappears_on_cleared_cookies | Happy Path: State reset | Dismiss ad, clear cookies, refresh | Modal reappears as expected. | High | **BVA** |

---

## Feature: Exit Intent
Simulates mouse movement behavior to trigger site-exit modals.
> **File:** test_exit_intent.py

| Test Case ID | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority | Testing Technique |
| --- | --- | --- | --- | --- | --- |
| test_exit_intent_happy_path_tc1 | Happy Path: Standard trigger | Dispatch JS `mouseleave`, click Close | Modal appears with correct title, then closes. | High | **State Transition** |
| test_exit_intent_one_time_trigger_tc2 | Happy Path: Refresh suppression | Trigger, close, attempt re-trigger | Modal does not appear a second time. | Medium | **State Transition** |
| test_exit_intent_no_trigger_within_bounds_tc3 | Sad Path: In-page movement | Move mouse to (100, 100) via `ActionChains` | Modal stays hidden. | Medium | **BVA** |
| test_exit_intent_overlay_blocking_tc4 | Robustness: Click interception | Trigger modal, click background link | `ElementClickInterceptedException` thrown. | High | **Negative Testing** |

---

## Feature: File Download
Validates browser download behavior by polling the local filesystem.
> **File:** test_file_download.py

| Test Case ID | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority | Testing Technique |
| --- | --- | --- | --- | --- | --- |
| test_tc1_download_success | Happy Path: Successful download | `driver.get(url)`, click first link | File is found in `test_downloads/` via polling. | High | **EP** |

---

## Feature: File Upload
Tests local file injection and empty state error handling.
> **File:** test_file_upload.py

| Test Case ID | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority | Testing Technique |
| --- | --- | --- | --- | --- | --- |
| test_tc1_upload_valid_file | Happy Path: Successful upload | Send path to `file-upload`, click Submit | "File Uploaded!" success header appears. | High | **EP** |
| test_tc2_upload_empty_submission | Sad Path: No file selected | Click Submit without input | "Internal Server Error" (500) caught. | Medium | **Negative Testing** |

---

## Feature: Floating Menu
Ensures UI navigation remains persistent during viewport scrolling.
> **File:** test_floating_menu.py

| Test Case ID | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority | Testing Technique |
| --- | --- | --- | --- | --- | --- |
| test_tc1_menu_visible_top | Happy Path: Initial visibility | Load page | `menu.is_displayed()` is True. | Low | **BVA** |
| test_tc2_menu_visible_on_scroll | Happy Path: Persistence on scroll | `scrollTo(0, scrollHeight)` | `menu.is_displayed()` remains True; links visible. | High | **State Transition** |
| test_tc3_menu_anchor_links_work | Happy Path: Anchor navigation | Click 'Home' link | URL hash updates to `#home`. | Medium | **EP** |

---

## Feature: Forgot Password
Tests form submission and server error resilience.
> **File:** test_forgot_password.py

| Test Case ID | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority | Testing Technique |
| --- | --- | --- | --- | --- | --- |
| test_tc1_valid_email_submission | Happy Path: Standard request | Input valid email, click Submit | Returns "Internal Server Error" or success text. | Medium | **EP** |
| test_tc2_empty_email_submission | Sad Path: Blank input | Clear email field, click Submit | Returns "Internal Server Error". | Medium | **BVA** |
| test_tc3_invalid_email_format | Sad Path: Malformed input | Input 'user_no_domain', click Submit | Returns "Internal Server Error". | Medium | **BVA** |

---

## Feature: Form Authentication
Comprehensive validation of standard login and logout flows.
> **File:** test_form_authentication.py

| Test Case ID | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority | Testing Technique |
| --- | --- | --- | --- | --- | --- |
| test_tc1_login_success | Happy Path: Successful login | tomsmith / SuperSecretPassword! | Redirect to `/secure`; success flash message. | Critical | **EP** |
| test_tc2_invalid_password | Sad Path: Wrong password | tomsmith / wrong | Flash message: "Your password is invalid!". | High | **Negative Testing** |
| test_tc3_invalid_username | Sad Path: Wrong username | wrong / SuperSecretPassword! | Flash message: "Your username is invalid!". | High | **Negative Testing** |
| test_tc4_empty_credentials | Sad Path: Blank fields | "" / "" | Flash message: "Your username is invalid!". | Medium | **Negative Testing** |
| test_tc7_logout_functionality | Happy Path: Successful logout | Login, then click Logout | Redirect back to `/login`; logout flash message. | High | **EP** |
| test_tc8_case_sensitive_username | Sad Path: Logic check | "TomSmith" (PascalCase) | Flash message: "Your username is invalid!". | Medium | **Negative Testing** |

---

## Feature: iFrame Isolation
Validates driver context switching and isolation between single iFrames.
> **File:** test_frame.py

| Test Case ID | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority | Testing Technique |
| --- | --- | --- | --- | --- | --- |
| test_iframe_happy_path_tc1 | Happy Path: iFrame interaction | `switch_to.frame("mce_0_ifr")`, inject text | Editor text matches injected payload. | High | **DOM Traversal / Context Isolation** |
| test_frame_context_leak_sad_path_tc2 | Sad Path: Context leak check | While in iframe, find main page `h3` | `NoSuchElementException` is caught. | High | **DOM Traversal / Context Isolation** |
| test_invalid_frame_access_sad_path_tc3 | Sad Path: Invalid target switch | `switch_to.frame("ghost_99")` | `NoSuchFrameException` is caught. | Medium | **Negative Testing** |

---

## Feature: Geolocation
Tests mocking of GPS coordinates via CDP (Chrome DevTools Protocol).
> **File:** test_geolocation.py

| Test Case ID | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority | Testing Technique |
| --- | --- | --- | --- | --- | --- |
| test_tc1_geolocation_reveal_coordinates | Happy Path: Coordinate population | `execute_cdp_cmd("Emulation.setGeolocationOverride", ...)` | Latitude/Longitude fields contain valid floats. | High | **State Transition** |
| test_tc2_geolocation_map_link | Happy Path: Dynamic map URL | Click "Where am I?", find `map-link` | URL contains "google" and the correct latitude. | Medium | **EP** |

---

## Feature: Horizontal Slider
Validates input range precision and boundary constraints.
> **File:** test_horizontal_slider.py

| Test Case ID | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority | Testing Technique |
| --- | --- | --- | --- | --- | --- |
| test_tc1_slider_increments_correctly | Happy Path: Precision check | `send_keys(Keys.ARROW_RIGHT)` | Value increments by exactly 0.5. | High | **EP** |
| test_tc2_slider_boundary_min | Happy Path: Bottom boundary | `send_keys(Keys.ARROW_LEFT)` x 15 | Slider value floor is 0. | Medium | **BVA** |

---

## Feature: Hovers
Simulates hover-triggered visibility using `ActionChains` and JS style-overrides.
> **File:** test_hovers.py

| Test Case ID | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority | Testing Technique |
| --- | --- | --- | --- | --- | --- |
| test_tc1_hover_user1 | Happy Path: Caption trigger | `move_to_element(fig[0])`, inject opacity | Caption header displays "name: user1". | High | **State Transition** |

---

## Feature: Infinite Scroll
Tests dynamic DOM expansion via AJAX-triggered scroll events.
> **File:** test_infinite_scroll.py

| Test Case ID | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority | Testing Technique |
| --- | --- | --- | --- | --- | --- |
| test_tc1_initial_content_load | Happy Path: Initial state | `presence_of_element_located(".jscroll-added")` | At least 1 block exists on page lead. | Low | **EP** |
| test_tc2_scroll_loads_more_content | Happy Path: Content growth | `scrollTo(0, scrollHeight)` loop 3 times | Paragraph count increases vs initial state. | High | **State Transition** |

---

## Feature: Number Inputs
Validates HTML5 number input constraints and arrow-key behaviors.
> **File:** test_inputs.py

| Test Case ID | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority | Testing Technique |
| --- | --- | --- | --- | --- | --- |
| test_tc1_valid_number_input | Happy Path: Numeric acceptance | `send_keys("500")`, then "-35" | Value attribute reflects input correctly. | High | **EP** |
| test_tc2_arrow_up_increment | Happy Path: Keyboard control | Input "10", `send_keys(Keys.ARROW_UP)` | Value increments to "11". | Medium | **State Transition** |
| test_tc3_arrow_down_decrement | Happy Path: Keyboard control | Input "10", `send_keys(Keys.ARROW_DOWN)` | Value decrements to "9". | Medium | **State Transition** |
| test_tc4_invalid_text_input | Sad Path: Type mismatch | `send_keys("abc")` | Value attribute remains empty (""). | High | **BVA** |

---

## Feature: JavaScript Error
Detects and logs client-side execution errors on page load.
> **File:** test_javascript_error.py

| Test Case ID | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority | Testing Technique |
| --- | --- | --- | --- | --- | --- |
| test_javascript_error_page_loads_tc1 | Happy Path: Error page load | `get(URL)`, wait for `body p` | Title is "Page with JavaScript errors on load". | High | **EP** |
| test_javascript_error_detection_tc2 | Sad Path: JS Error catch | `execute_script("return window.JSErrorOccurred;")` | Returns True (JS script failed on load). | Critical | **Negative Testing** |

---

## Feature: JQuery UI Menus
Validates complex nested navigation with headless hover workarounds.
> **File:** test_jquery_ui_menus.py

| Test Case ID | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority | Testing Technique |
| --- | --- | --- | --- | --- | --- |
| test_jquery_menu_enabled_pdf_tc1 | Happy Path: Nested navigation | Inject `display:block`, click PDF | File download initiated/navigated. | High | **State Transition** |
| test_jquery_menu_disabled_not_clickable_tc3 | Sad Path: Disabled item | Locate 'Disabled' LI | Has class `ui-state-disabled`; not interactable. | Medium | **Negative Testing** |
| test_jquery_menu_disabled_no_submenu_tc4 | Sad Path: Hidden sub-menu | Locate child `<ul>` of 'Disabled' item | Child `<ul>` exists but `is_displayed()` is False. | High | **BVA** |

---

## Feature: JS Alerts
Handles browser-native Modal, Confirm, and Prompt dialogs.
> **File:** test_js_alerts.py

| Test Case ID | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority | Testing Technique |
| --- | --- | --- | --- | --- | --- |
| test_tc1_accept_js_alert | Happy Path: Accept Alert | Click `jsAlert()`, `alert.accept()` | #result shows "You successfully clicked...". | High | **State Transition** |
| test_tc2_accept_js_confirm | Happy Path: Accept Confirm | Click `jsConfirm()`, `alert.accept()` | #result shows "You clicked: Ok". | High | **State Transition** |
| test_tc3_dismiss_js_confirm | Sad Path: Dismiss Confirm | Click `jsConfirm()`, `alert.dismiss()` | #result shows "You clicked: Cancel". | Medium | **State Transition** |

---

## Feature: Key Presses
Validates the mapping of browser-reflected keyboard events.
> **File:** test_key_presses.py

| Test Case ID | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority | Testing Technique |
| --- | --- | --- | --- | --- | --- |
| test_tc1_special_keyboard_keys | Happy Path: Logic keys | Send SPACE, ENTER, TAB, ESCAPE | Result echoes correct key name. | High | **EP** |
| test_tc2_alphanumeric_keyboard_keys | Happy Path: Alphanumeric | Send "a", "Z", "7" | Result echoes uppercase char/mapped name. | Medium | **EP** |

---

## Feature: Large & Deep DOM
Tests for performance and selector reliability in massive DOM trees.
> **File:** test_large_deep_dom.py

| Test Case ID | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority | Testing Technique |
| --- | --- | --- | --- | --- | --- |
| test_large_dom_deep_element_tc1 | Happy Path: Deep nesting | `find_element(By.ID, "no-siblings")` | Element is present (100+ nested DIVs). | High | **EP** |
| test_large_dom_boundary_cell_tc2 | Happy Path: BVA grid check | Discover `sibling-N.M` IDs via JS | Largest boundary ID is correctly identified. | Medium | **BVA** |
| test_large_dom_invalid_id_sad_path_tc3 | Sad Path: Missing element | Wait for `#large-999-999` | `TimeoutException` is caught. | Low | **Negative Testing** |

---

## Feature: Multiple Windows
Tests browser tab management and handle-based context switching.
> **File:** test_multiple_windows.py

| Test Case ID | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority | Testing Technique |
| --- | --- | --- | --- | --- | --- |
| test_multiple_windows_switch_happy_path_tc1 | Happy Path: Switch to tab | Click link, switch to `window_handle[1]` | New window contains "New Window" text. | High | **DOM Traversal / Context Isolation** |
| test_multiple_windows_isolation_sad_path_tc2 | Sad Path: Context boundary | Try access new tab without `switch_to` | `NoSuchElementException` is caught. | High | **DOM Traversal / Context Isolation** |
| test_invalid_window_handle_sad_path_tc3 | Sad Path: Ghost handle | `switch_to.window("ghost_tab_999")` | `NoSuchWindowException` is caught. | Medium | **Negative Testing** |

---

## Feature: Nested Frames
Validates multi-level DOM frame traversal and sibling isolation.
> **File:** test_nested_frames.py

| Test Case ID | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority | Testing Technique |
| --- | --- | --- | --- | --- | --- |
| test_nested_frames_top_traversal_tc1 | Happy Path: Deep traversal | `frame-top` -> `frame-left/middle/right` | Each frame contains its specific label text. | High | **DOM Traversal / Context Isolation** |
| test_nested_frames_bottom_traversal_tc2 | Happy Path: Root traversal | `default_content()` -> `frame-bottom` | Bottom frame reflects "BOTTOM" text. | High | **DOM Traversal / Context Isolation** |
| test_nested_frames_sibling_isolation_tc3 | Sad Path: Illegal jump | While in `left`, jump directly to `right` | `NoSuchFrameException` is caught. | High | **DOM Traversal / Context Isolation** |

---

## Feature: Notification Messages
Validates flash alerts with resilience to server-side typos.
> **File:** test_notification_messages.py

| Test Case ID | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority | Testing Technique |
| --- | --- | --- | --- | --- | --- |
| test_notification_click_success_tc1 | Happy Path: Trigger message | Click "Click here", wait for #flash | Flash message text contains 'Action'. | High | **EP** |
| test_notification_message_typo_resilience_tc3 | Robustness: Typo handling | Scan message vs. `VALID_MESSAGES` set | Matches either "successful" or typo variant. | High | **BVA** |

---

## Feature: Redirect Link
Verifies HTTP redirect chain tracking from origin to destination.
> **File:** test_redirect_link.py

| Test Case ID | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority | Testing Technique |
| --- | --- | --- | --- | --- | --- |
| test_redirect_link_url_change_tc1 | Happy Path: URL transition | Click `a[href='redirect']` | URL contains "status_codes". | Critical | **EP** |
| test_redirect_invalid_endpoint_tc3 | Sad Path: Direct invalid navigation | `get("/redirect/nonexistent")` | Landing page does NOT contain "Status Codes". | Medium | **Negative Testing** |
| test_redirect_link_absent_on_wrong_page_tc4 | Sad Path: Reverse context check | Load `/status_codes` directly | Redirect link is correctly absent. | Low | **Negative Testing** |

---

## Feature: Secure File Download
Validates authentication-protected resource access.
> **File:** test_secure_file_download.py

| Test Case ID | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority | Testing Technique |
| --- | --- | --- | --- | --- | --- |
| test_secure_download_auth_happy_path_tc1 | Happy Path: Auth bypass | Embed `admin:admin` in URL | Secure file links become visible in DOM. | High | **EP** |
| test_secure_download_unauth_sad_path_tc2 | Sad Path: Unauth access | Navigate WITHOUT credentials | `TimeoutException` caught (access denied). | High | **Negative Testing** |

---

## Feature: Shadow DOM
Tests for shadow-boundary penetration techniques.
> **File:** test_shadow_dom.py

| Test Case ID | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority | Testing Technique |
| --- | --- | --- | --- | --- | --- |
| test_shadow_dom_access_via_shadow_root_tc1 | Happy Path: Selenium 4 piercing | `shadow_host.shadow_root.find_element()` | Inner shadow text is retrieved. | High | **DOM Traversal / Context Isolation** |
| test_shadow_dom_access_via_js_tc2 | Happy Path: JS piercing | `querySelector('host').shadowRoot` | JS retrieves content across boundary. | High | **DOM Traversal / Context Isolation** |
| test_shadow_dom_xpath_cannot_pierce_tc3 | Sad Path: Encapsulation check | Global XPath search for inner element | `TimeoutException` (shadow DOM is opaque). | Medium | **Negative Testing** |

---

## Feature: Shifting Content
Validates layout stability and DOM presence during CSS animations.
> **File:** test_shifting_content.py

| Test Case ID | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority | Testing Technique |
| --- | --- | --- | --- | --- | --- |
| test_tc1_menu_renders_successfully_despite_shifting | Happy Path: Animation resilience | Wait for menu items, verify enabled | At least 5 menu items load and are clickable. | High | **State Transition** |

---

## Feature: Slow Resources
Verifies handling of high-latency resource loading.
> **File:** test_slow_resources.py

| Test Case ID | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority | Testing Technique |
| --- | --- | --- | --- | --- | --- |
| test_slow_resources_full_load_tc1 | Happy Path: Generous timing | `WebDriverWait(30)` for heading | Heading eventually becomes visible. | High | **BVA** |
| test_slow_resources_perf_entry_exists_tc2 | Happy Path: API audit | Check `window.performance` | Entry exists; duration > 0ms. | Medium | **EP** |
| test_slow_resources_short_timeout_bva_tc2_retry | Sad Path: BVA timeout | Wait with 1s timeout | `TimeoutException` is caught immediately. | High | **BVA** |

---

## Feature: Sortable Data Tables
Validates dynamic sorting algorithms on complex tabular data.
> **File:** test_sortable_data_tables.py

| Test Case ID | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority | Testing Technique |
| --- | --- | --- | --- | --- | --- |
| test_sortable_tables_sort_lastname_asc_tc1 | Happy Path: ASC sort | Click header once, extract column | Column matches `sorted()` order. | High | **EP** |
| test_sortable_tables_sort_lastname_desc_tc2 | Happy Path: DESC sort | Click header twice | Column matches `sorted(reverse=True)`. | High | **EP** |
| test_sortable_tables_out_of_bounds_column_tc4 | Sad Path: Index safety | Attempt to extract column 99 | Returns empty list gracefully. | Low | **BVA** |

---

## Feature: Status Codes
Verifies page response handlers for various HTTP return states.
> **File:** test_status_codes.py

| Test Case ID | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority | Testing Technique |
| --- | --- | --- | --- | --- | --- |
| test_tc1_status_code_200_ok | Happy Path: HTTP 200 | Click "200" link | Body contains "page returned a 200". | High | **EP** |
| test_tc4_status_code_500_server_error | Happy Path: HTTP 500 | Click "500" link | Body contains "page returned a 500". | High | **EP** |

---

## Feature: Typos
Analyzes random typographical variances using probabilistic auditing.
> **File:** test_typos.py

| Test Case ID | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority | Testing Technique |
| --- | --- | --- | --- | --- | --- |
| test_typos_refresh_until_correct_tc1 | Happy Path: Variance audit | Refresh until "won't" found (max 10) | Correct spelling eventually appears. | Low | **BVA** |
| test_typos_detect_known_typo_tc2 | Happy Path: Bug classification | Audit for "won,t" | Known defect identified/logged as A/B variant. | Medium | **EP** |
| test_typos_page_structure_robustness_tc3 | Happy Path: Layout consistency | Count `<p>` tags across variations | Always exactly 2 paragraphs in .example. | Medium | **BVA** |

---

## Feature: WYSIWYG Editor (TinyMCE)
Validates rich-text editor functionality with read-only bypass techniques.
> **File:** test_wysiwyg_editor.py

| Test Case ID | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority | Testing Technique |
| --- | --- | --- | --- | --- | --- |
| test_wysiwyg_js_injection_happy_path_tc1 | Happy Path: Read-only bypass | Inject HTML into #tinymce body | Payload appears despite warning overlay. | Critical | **State Transition** |
| test_wysiwyg_readonly_alert_sad_path_tc2 | Sad Path: Warning detection | Check for `.tox-notification--warning` | Overlay present when API limit hit. | Medium | **BVA** |
| test_wysiwyg_toolbar_visibility_happy_path_tc3 | Happy Path: Toolbar audit | Find Bold/Italic buttons via ARIA | Buttons are visible in primary document. | High | **EP** |
| test_wysiwyg_context_isolation_sad_path_tc4 | Sad Path: Frame isolation | Enter iframe, search for toolbar | `NoSuchElementException` (buttons outside). | High | **DOM Traversal / Context Isolation** |
