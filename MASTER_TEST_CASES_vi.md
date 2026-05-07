# BỘ TEST CASE TỰ ĐỘNG HÓA TỔNG HỢP

> **Dự án:** The Internet – Bộ kiểm thử tự động hóa Selenium cho Herokuapp
> **Công nghệ:** Python · Selenium WebDriver · unittest
> **Tổng số tính năng được kiểm thử:** 44
> **Cập nhật lần cuối:** 2026-05-07

---

## Tính năng: Kiểm thử A/B (Phân nhóm người dùng)
> **Tệp:** test_ab_testing.py

| Mã Test Case | Tên Hàm | Kỹ thuật | Mô tả Kịch bản | Dữ liệu / Hành động | Kết quả mong đợi | Mức độ ưu tiên |
|---|---|---|---|---|---|---|
| TC_AB_01 | `test_ab_testing_header_variation_tc1` | Phân vùng tương đương - Luồng thành công | Điều hướng đến trang kiểm thử A/B và xác minh rằng tiêu đề trang hiển thị một trong hai biến thể thí nghiệm hợp lệ đã biết. | `Navigate to /abtest` → `Wait for EC.visibility_of_element_located((By.TAG_NAME, "h3"))` → `assertIn(text, VALID_HEADERS)` | Tiêu đề trang hiển thị "A/B Test Control" hoặc "A/B Test Variation 1", xác nhận thí nghiệm đang chạy đúng. | Cao |
| TC_AB_02 | `test_ab_testing_paragraph_presence_tc2` | Phân vùng tương đương - Luồng thành công | Truy cập trang kiểm thử A/B và xác nhận đoạn mô tả thông tin luôn hiển thị bất kể biến thể nào được phục vụ. | `Navigate to /abtest` → `Wait for XPath //p[contains(text(),'Also known as split testing')]` → `assertTrue(paragraph.is_displayed())` | Đoạn văn mô tả kiểm thử phân chia hiển thị trên trang ở tất cả các biến thể. | Trung bình |
| TC_AB_03 | `test_ab_testing_optout_cookie_tc3` | Kiểm thử âm - Độ bền | Đặt cookie từ chối trước khi tải trang A/B và xác minh hệ thống loại người dùng ra khỏi thí nghiệm. | `Navigate to /abtest` → `add_cookie({'name': 'optimizelyOptOut', 'value': 'true'})` → `driver.refresh()` → `assertEqual(text, "No A/B Test")` | Sau khi đặt cookie từ chối, tiêu đề trang hiển thị "No A/B Test", xác nhận người dùng đã bị loại khỏi tất cả biến thể thí nghiệm. | Cao |
| TC_AB_04 | `test_ab_testing_reset_cookie_valid_variant_tc4` | Phân tích giá trị biên - Độ bền | Lặp lại chu kỳ xóa cookie và tải lại trang 10 lần để xác minh hệ thống luôn trả về biến thể A/B hợp lệ và không bị lỗi. | `Loop 10x: Navigate to /abtest` → `delete_all_cookies()` → `driver.refresh()` → `assertIn(text, VALID_HEADERS)` | Mỗi lần tải lại sau khi xóa cookie đều trả về tiêu đề biến thể A/B đã biết, không có lỗi hoặc trạng thái bất ngờ. | Trung bình |

---

## Tính năng: Thêm / Xóa phần tử động
> **Tệp:** test_add_remove_elements.py

| Mã Test Case | Tên Hàm | Kỹ thuật | Mô tả Kịch bản | Dữ liệu / Hành động | Kết quả mong đợi | Mức độ ưu tiên |
|---|---|---|---|---|---|---|
| TC_ARE_01 | `test_tc1_add_single_element` | Phân vùng tương đương - Luồng thành công | Nhấp nút "Add Element" một lần và xác minh rằng đúng một nút xóa xuất hiện trên trang. | `Navigate to /add_remove_elements/` → `Click XPath //button[text()='Add Element']` → `find_elements(By.CLASS_NAME, "added-manually")` → `assertEqual(len, 1)` | Đúng một nút "Delete" được hiển thị trên trang sau một lần nhấp. | Cao |
| TC_ARE_02 | `test_tc2_remove_single_element` | Phân vùng tương đương - Luồng thành công | Thêm một phần tử rồi xóa ngay, xác minh trang trở về trạng thái trống. | `Navigate` → `Click Add Element` → `Click Delete button` → `Wait for EC.staleness_of(delete_btn)` → `assertEqual(len(remaining), 0)` | Sau khi nhấp xóa, nút biến mất và trang trở về trạng thái sạch. | Cao |
| TC_ARE_03 | `test_tc3_add_multiple_elements` | Phân vùng tương đương - Luồng thành công | Nhấp "Add Element" năm lần liên tiếp để xác minh DOM tích lũy đúng nhiều phần tử động. | `Navigate` → `Click Add Element 5×` → `Wait for EC.presence_of_all_elements_located(By.CLASS_NAME, "added-manually")` → `assertEqual(len, 5)` | Năm nút "Delete" riêng biệt được tạo ra, mỗi nút hiển thị và được thêm đúng vào trang. | Trung bình |
| TC_ARE_04 | `test_tc4_remove_all_elements_dynamically` | Phân tích giá trị biên - Luồng thất bại | Thêm ba phần tử rồi xóa từng cái, xác minh DOM hoàn toàn trống sau mỗi chu kỳ xóa. | `Navigate` → `Click Add Element 3×` → `For each btn: btn.click()` → `Wait for EC.staleness_of(btn)` → `assertEqual(len(remaining), 0)` | Sau khi xóa tất cả ba phần tử, trang hoàn toàn trống với không còn nút xóa nào. | Trung bình |

---

## Tính năng: Xác thực cơ bản (Basic Auth)
> **Tệp:** test_basic_auth.py

| Mã Test Case | Tên Hàm | Kỹ thuật | Mô tả Kịch bản | Dữ liệu / Hành động | Kết quả mong đợi | Mức độ ưu tiên |
|---|---|---|---|---|---|---|
| TC_BA_01 | `test_tc1_success` | Phân vùng tương đương - Luồng thành công | Đăng nhập với tên người dùng và mật khẩu đúng qua Basic Auth nhúng URL và xác minh thông báo thành công xuất hiện. | `Navigate to https://admin:admin@the-internet.herokuapp.com/basic_auth` → `find_element(By.TAG_NAME, "body")` → `assertTrue(is_authenticated())` | Thông báo chúc mừng được hiển thị, xác nhận người dùng đã được cấp quyền truy cập. | Nghiêm trọng |
| TC_BA_02 | `test_tc2_wrong_password` | Kiểm thử âm - Luồng thất bại | Thử đăng nhập với tên người dùng đúng nhưng mật khẩu sai và xác minh quyền truy cập bị từ chối. | `Navigate to https://admin:wrongpassword@.../basic_auth` → `assertFalse(is_authenticated())` | Thông báo thành công không xuất hiện; người dùng bị chặn đúng cách khỏi trang bảo mật. | Nghiêm trọng |
| TC_BA_03 | `test_tc3_invalid_username` | Kiểm thử âm - Luồng thất bại | Thử đăng nhập với tên người dùng không tồn tại và xác minh hệ thống từ chối yêu cầu. | `Navigate to https://fakeuser:admin@.../basic_auth` → `assertFalse(is_authenticated())` | Xác thực thất bại và thông báo thành công vắng mặt, xác nhận hệ thống kiểm tra sự tồn tại của tên người dùng. | Cao |
| TC_BA_04 | `test_tc4_empty_both` | Kiểm thử âm - Luồng thất bại | Gửi yêu cầu xác thực với cả hai trường tên người dùng và mật khẩu hoàn toàn trống. | `Navigate to https://:@.../basic_auth` → `assertFalse(is_authenticated())` | Quyền truy cập bị từ chối khi không cung cấp thông tin xác thực, và không có thông báo thành công. | Cao |
| TC_BA_05 | `test_tc5_case_sensitivity_user` | Kiểm thử âm - Trường hợp biên | Attempt to log in using a username with incorrect capitalisation (e.g., "Admin" instead of "admin") to confirm the system is case-sensitive. | `Navigate to https://Admin:admin@.../basic_auth` → `assertFalse(is_authenticated())` | The system rejects the mixed-case username, confirming that authentication is case-sensitive for usernames. | Trung bình |
| TC_BA_06 | `test_tc6_case_sensitivity_pass` | Kiểm thử âm - Trường hợp biên | Attempt to log in with a password in all uppercase letters to confirm the password field is also case-sensitive. | `Navigate to https://admin:ADMIN@.../basic_auth` → `assertFalse(is_authenticated())` | The system rejects the uppercase password, confirming that authentication is case-sensitive for passwords. | Trung bình |
| TC_BA_07 | `test_tc7_special_chars_password` | Kiểm thử âm - Độ bền | Attempt login with a password containing special characters (e.g., "@", ":") to verify the URL encoding mechanism handles them safely without crashing. | `urllib.parse.quote("p@ss:word#123")` → `Navigate to encoded URL` → `Log result without assertion block` | The application handles the special-character password gracefully via URL encoding, without throwing an unhandled error. | Trung bình |
| TC_BA_08 | `test_tc8_sql_injection_attempt` | Kiểm thử bảo mật - Độ bền | Inject a basic SQL injection string as the username to verify the authentication layer is not vulnerable to this attack. | `urllib.parse.quote("' OR '1'='1")` → `Navigate` → `assertFalse(is_authenticated())` | The SQL injection string is treated as a literal invalid credential and access is denied, confirming the system is not vulnerable. | Cao |
| TC_BA_09 | `test_tc9_very_long_credentials` | Kiểm thử âm - Độ bền | Submit an extremely long string (1000 characters) as both username and password to test for buffer overflow vulnerabilities. | `long_str = "a" * 1000` → `Navigate to encoded URL` → `assertFalse(is_authenticated())` | The system handles the oversized credentials gracefully and denies access, without crashing or hanging. | Trung bình |

---

## Tính năng: Hình ảnh bị lỗi
> **Tệp:** test_broken_images.py

| Mã Test Case | Tên Hàm | Kỹ thuật | Mô tả Kịch bản | Dữ liệu / Hành động | Kết quả mong đợi | Mức độ ưu tiên |
|---|---|---|---|---|---|---|
| TC_BI_01 | `test_tc1_verify_total_images_on_page` | Phân vùng tương đương - Luồng thành công | Tải trang hình ảnh bị lỗi và xác minh có ít nhất ba phần tử hình ảnh trong bố cục trang. | `Navigate to /broken_images` → `Wait for EC.presence_of_all_elements_located(By.TAG_NAME, "img")` → `assertTrue(len(images) >= 3)` | Ít nhất ba phần tử hình ảnh được tìm thấy trong DOM, xác nhận cấu trúc cơ bản còn nguyên vẹn. | Trung bình |
| TC_BI_02 | `test_tc2_identify_broken_images` | Phân vùng tương đương - Luồng thất bại | Thực hiện yêu cầu HTTP cho từng URL hình ảnh và xác định chính xác những hình ảnh trả về mã trạng thái không phải 200. | `find_elements(By.TAG_NAME, "img")` → `For each: requests.get(src, timeout=5)` → `assertEqual(len(broken_imgs), 2)` | Đúng hai hình ảnh được xác định là bị lỗi (phản hồi HTTP không phải 200), khớp với lỗi đã biết trên trang demo này. | Cao |
| TC_BI_03 | `test_tc3_identify_valid_images` | Phân vùng tương đương - Luồng thành công | Xác minh rằng script xác định đúng những hình ảnh tải thành công (HTTP 200 OK). | `find_elements(By.TAG_NAME, "img")` → `For each: requests.get(src)` → `assertTrue(len(valid_imgs) >= 1)` | Ít nhất một hình ảnh trên trang trả về phản hồi 200 OK thành công và được xác định là hình ảnh hợp lệ. | Trung bình |

---

## Tính năng: DOM phức tạp
> **Tệp:** test_challenging_dom.py

| Mã Test Case | Tên Hàm | Kỹ thuật | Mô tả Kịch bản | Dữ liệu / Hành động | Kết quả mong đợi | Mức độ ưu tiên |
|---|---|---|---|---|---|---|
| TC_CD_01 | `test_dynamic_buttons_tc1` | Phân vùng tương đương - Luồng thành công | Nhấp vào nút cảnh báo đỏ (có ID thay đổi động) bằng bộ chọn class CSS ổn định và xác minh nó vẫn hiển thị sau khi DOM tải lại. | `Navigate to /challenging_dom` → `Click CSS_SELECTOR ".button.alert"` → `Wait for EC.presence_of_element_located(".button.alert")` → `assertTrue(is_displayed())` | The red button is found and clickable without relying on a volatile ID, and it remains visible after the post-click DOM refresh. | Cao |
| TC_CD_02 | `test_table_ep_mid_tc2` | Phân vùng tương đương - Luồng thành công | Đọc và xác minh nội dung dữ liệu từ hàng thứ 5 (giữa) của bảng để xác nhận lưới dữ liệu hiển thị đúng. | `Navigate to /challenging_dom` → `Wait for XPath //table/tbody/tr[5]` → `assertTrue("Iuvaret4" in text or "Apeirian4" in text)` | Row 5 contains non-empty text with the expected middle-range data values ("Iuvaret4" or "Apeirian4"). | Trung bình |
| TC_CD_03 | `test_table_bva_min_tc3` | Phân tích giá trị biên - Luồng thành công | Đọc và xác minh nội dung từ hàng thứ 1 (giới hạn tối thiểu) của bảng dữ liệu. | `Navigate to /challenging_dom` → `Wait for XPath //table/tbody/tr[1]` → `assertTrue("Iuvaret0" in text or "Apeirian0" in text)` | The first row contains the expected minimum-index data values, confirming the table renders correctly from the top. | Trung bình |
| TC_CD_04 | `test_table_bva_max_tc4` | Phân tích giá trị biên - Luồng thành công | Đọc và xác minh nội dung từ hàng thứ 10 (giới hạn tối đa) của bảng dữ liệu. | `Navigate to /challenging_dom` → `Wait for XPath //table/tbody/tr[10]` → `assertTrue("Iuvaret9" in text or "Apeirian9" in text)` | The last row contains the expected maximum-index data values, confirming the table renders all 10 rows correctly. | Trung bình |
| TC_CD_05 | `test_table_negative_out_of_bounds_tc5` | Kiểm thử âm - Luồng thất bại | Cố gắng truy cập hàng thứ 11 không tồn tại và xác minh hệ thống xử lý phần tử thiếu một cách nhẹ nhàng. | `WebDriverWait(driver, 2)` → `Try to locate XPath //table/tbody/tr[11]` → `Catch TimeoutException or NoSuchElementException` | A timeout or element-not-found exception is caught gracefully, confirming the table has exactly 10 rows and no more. | Trung bình |
| TC_CD_06 | `test_canvas_verification_tc6` | Phân vùng tương đương - Luồng thành công | Xác minh phần tử canvas HTML hiện diện và hiển thị trên trang DOM phức tạp. | `Navigate to /challenging_dom` → `Wait for CSS_SELECTOR "canvas#canvas"` → `assertTrue(canvas.is_displayed())` | The canvas element is rendered and visible on the page, confirming the dynamic rendering engine functions correctly. | Thấp |
| TC_CD_07 | `test_table_action_links_tc7` | Phân vùng tương đương - Luồng thành công | Nhấp vào liên kết hành động "edit" và "delete" trong một hàng bảng cụ thể và xác minh mỗi lần nhấp cập nhật đúng đoạn URL. | `Click XPath //table/tbody/tr[3]/td[7]/a[@href='#edit']` → `assertIn("#edit", current_url)` → `Click a[@href='#delete']` → `assertIn("#delete", current_url)` | After each click, the URL fragment updates to "#edit" and then "#delete", confirming the action links are functional. | Trung bình |
| TC_CD_08 | `test_tc8_dynamic_id_shift` | Phân vùng tương đương - Độ bền | Ghi lại ID của nút xanh trước khi nhấp, sau đó xác minh ID đã thay đổi sau khi trang tải lại động, chứng minh DOM thực sự biến động. | `Locate ".button:not(.alert):not(.success)"` → `old_id = get_attribute("id")` → `Click` → `Wait for EC.staleness_of()` → `new_id = get_attribute("id")` → `assertNotEqual(old_id, new_id)` | The button's ID value is different before and after the click, confirming that the page uses dynamically generated element IDs. | Cao |

---

## Tính năng: Hộp kiểm (Checkbox)
> **Tệp:** test_checkbox.py

| Mã Test Case | Tên Hàm | Kỹ thuật | Mô tả Kịch bản | Dữ liệu / Hành động | Kết quả mong đợi | Mức độ ưu tiên |
|---|---|---|---|---|---|---|
| TC_CB_01 | `test_tc1_default_state_validation` | Phân vùng tương đương - Luồng thành công | Tải trang hộp kiểm và xác minh trạng thái mặc định: hộp kiểm đầu tiên chưa được chọn và hộp thứ hai đã được chọn. | `Navigate to /checkboxes` → `XPath //*[@id="checkboxes"]/input[1]` and `input[2]` → `assertFalse(cb1.is_selected())` → `assertTrue(cb2.is_selected())` | Hộp kiểm 1 chưa được chọn và Hộp kiểm 2 đã được chọn theo mặc định, đúng như thiết kế của trang. | Cao |
| TC_CB_02 | `test_tc2_check_first_checkbox` | Phân vùng tương đương - Luồng thành công | Tương tác với hộp kiểm đầu tiên (ban đầu chưa chọn) bằng cách nhấp vào, sau đó xác minh nó đã ở trạng thái được chọn. | `Navigate to /checkboxes` → `If not cb1.is_selected(): cb1.click()` → `assertTrue(cb1.is_selected())` | Hộp kiểm đầu tiên chuyển từ chưa chọn sang đã chọn sau khi được nhấp. | Cao |
| TC_CB_03 | `test_tc3_uncheck_second_checkbox` | Phân vùng tương đương - Luồng thành công | Tương tác với hộp kiểm thứ hai (ban đầu đã chọn) bằng cách nhấp vào, sau đó xác minh nó chuyển sang trạng thái chưa chọn. | `Navigate to /checkboxes` → `If cb2.is_selected(): cb2.click()` → `assertFalse(cb2.is_selected())` | Hộp kiểm thứ hai chuyển từ đã chọn sang chưa chọn sau khi được nhấp. | Cao |
| TC_CB_04 | `test_tc4_toggle_both_checkboxes` | Kiểm thử âm - Độ bền | Lặp đi lặp lại chuyển đổi cả hai hộp kiểm để xác minh trạng thái đã chọn/chưa chọn vẫn ổn định và nhất quán. | `cb1.click()` → `assertTrue(cb1)` → `cb1.click()` → `assertFalse(cb1)` → Repeat for `cb2` | Cả hai hộp kiểm chuyển đổi đúng giữa trạng thái đã chọn và chưa chọn qua nhiều lần nhấp liên tiếp mà không bị hỏng trạng thái. | Trung bình |

---

## Tính năng: Menu ngữ cảnh (Chuột phải)
> **Tệp:** test_context_menu.py

| Mã Test Case | Tên Hàm | Kỹ thuật | Mô tả Kịch bản | Dữ liệu / Hành động | Kết quả mong đợi | Mức độ ưu tiên |
|---|---|---|---|---|---|---|
| TC_CM_01 | `test_tc1_context_menu_success_and_cleanup` | Phân vùng tương đương - Luồng thành công | Nhấp chuột phải trong vùng điểm nóng được chỉ định và xác minh thông báo JavaScript alert đúng xuất hiện, sau đó đóng sạch. | `Navigate to /context_menu` → `ActionChains.context_click(#hot-spot)` → `Wait for EC.alert_is_present()` → `assertEqual(alert.text, "You selected a context menu")` → `alert.accept()` | Thông báo alert đọc "You selected a context menu" và được đóng thành công mà không để lại trạng thái dư thừa. | Cao |
| TC_CM_02 | `test_tc2_left_click_ignores_menu` | Kiểm thử âm - Luồng thất bại | Thực hiện nhấp chuột trái thông thường (thay vì chuột phải) trên điểm nóng và xác minh không có JavaScript alert nào được kích hoạt. | `Navigate to /context_menu` → `ActionChains.click(#hot-spot)` → `WebDriverWait(driver, 2)` → `Catch TimeoutException` | Không có alert nào được kích hoạt bởi nhấp chuột trái thông thường, xác nhận tính năng chỉ được gắn với sự kiện chuột phải. | Trung bình |
| TC_CM_03 | `test_tc3_boundary_click_outside_hotspot` | Phân tích giá trị biên - Độ bền | Nhấp chuột phải bên ngoài vùng điểm nóng (trên tiêu đề trang) và xác minh không có alert nào bị kích hoạt nhầm. | `Navigate to /context_menu` → `ActionChains.context_click(By.TAG_NAME, "h3")` → `WebDriverWait(driver, 2)` → `Catch TimeoutException` | Không có alert nào xuất hiện khi nhấp chuột phải bên ngoài điểm nóng, xác nhận trình nghe sự kiện được giới hạn đúng trong vùng chỉ định. | Trung bình |

---

## Tính năng: Xác thực Digest
> **Tệp:** test_digest_auth.py

| Mã Test Case | Tên Hàm | Kỹ thuật | Mô tả Kịch bản | Dữ liệu / Hành động | Kết quả mong đợi | Mức độ ưu tiên |
|---|---|---|---|---|---|---|
| TC_DA_01 | `test_digest_auth_happy_path_tc1` | Phân vùng tương đương - Luồng thành công | Đăng nhập vào trang được bảo vệ bởi Digest Auth bằng thông tin xác thực hợp lệ và xác minh thông báo xác nhận thành công xuất hiện. | `urllib.parse.quote("admin")` + `urllib.parse.quote("admin")` → `Navigate to https://admin:admin@.../digest_auth` → `Wait for XPath //p[contains(text(),'Congratulations')]` | Thông báo "Congratulations! You must have the proper credentials." hiển thị, xác nhận Digest Authentication thành công. | Nghiêm trọng |
| TC_DA_02 | `test_digest_auth_invalid_creds_tc2` | Kiểm thử âm - Luồng thất bại | Cố gắng truy cập trang Digest Auth với mật khẩu sai và xác minh trang bị từ chối. | `Navigate to https://admin:wrong@.../digest_auth` → `_assert_success_absent(timeout=2)` → `assertNotIn(SUCCESS_TEXT, body_text)` | Thông báo thành công không xuất hiện; mật khẩu sai bị Digest Authentication từ chối đúng cách. | Nghiêm trọng |
| TC_DA_03 | `test_digest_auth_unauthorized_tc3` | Kiểm thử bảo mật - Luồng thất bại | Cố gắng truy cập trang Digest Auth mà không có bất kỳ thông tin xác thực nào trong URL và xác minh quyền truy cập bị chặn. | `Navigate to https://the-internet.herokuapp.com/digest_auth` (no credentials)` → `_assert_success_absent(timeout=2)` | Quyền truy cập bị từ chối và không có thông báo thành công, xác nhận điểm cuối được bảo vệ đúng cách và không thể truy cập mà không có thông tin xác thực. | Nghiêm trọng |
| TC_DA_04 | `test_digest_auth_special_chars_tc4` | Kiểm thử âm - Độ bền | Kiểm tra rằng mật khẩu chứa ký tự đặc biệt "@" được mã hóa URL an toàn trước khi truyền và dẫn đến từ chối đúng. | `urllib.parse.quote("admin@123", safe="")` → `assertIn("%40", encoded_pass)` → `Navigate to constructed URL` → `_assert_success_absent(timeout=2)` | Ký tự "@" được mã hóa đúng thành "%40" trong URL. Mật khẩu được truyền an toàn và thông tin xác thực không hợp lệ bị từ chối đúng cách. | Cao |

---

## Tính năng: Phần tử biến mất ngẫu nhiên
> **Tệp:** test_disappearing_elements.py

| Mã Test Case | Tên Hàm | Kỹ thuật | Mô tả Kịch bản | Dữ liệu / Hành động | Kết quả mong đợi | Mức độ ưu tiên |
|---|---|---|---|---|---|---|
| TC_DE_01 | `test_tc1_verify_permanent_links` | Phân vùng tương đương - Luồng thành công | Tải trang và xác nhận rằng bốn liên kết điều hướng cố định (Home, About, Contact Us, Portfolio) luôn hiển thị. | `Navigate to /disappearing_elements` → `For each text in ["Home","About","Contact Us","Portfolio"]: Wait for EC.presence_of_element_located(By.LINK_TEXT, text)` → `assertTrue(is_displayed())` | Tất cả bốn liên kết điều hướng cố định hiển thị trên mỗi lần tải trang không có ngoại lệ. | Cao |
| TC_DE_02 | `test_tc2_gallery_appears_on_refresh` | Phân vùng tương đương - Độ bền | Làm mới trang tối đa năm lần để bắt liên kết "Gallery" xuất hiện ngẫu nhiên, nhấp vào nó và xác nhận nó dẫn đến trang 404. | `Loop up to 5×: driver.refresh()` → `find_elements(By.LINK_TEXT, "Gallery")` → `If found: click()` → `assertIn("Not Found", page_source)` | Liên kết "Gallery" cuối cùng được phát hiện qua nhiều lần làm mới, có thể nhấp và điều hướng đúng đến trang 404 Not Found. | Trung bình |

---

## Tính năng: Kéo và thả
> **Tệp:** test_drag_and_drop.py

| Mã Test Case | Tên Hàm | Kỹ thuật | Mô tả Kịch bản | Dữ liệu / Hành động | Kết quả mong đợi | Mức độ ưu tiên |
|---|---|---|---|---|---|---|
| TC_DD_01 | `test_tc1_drag_a_to_b` | Phân vùng tương đương - Luồng thành công | Kéo Khối A lên Khối B và xác minh hai khối hoán đổi nhãn trực quan ("A" thành "B" và ngược lại). | `Navigate to /drag_and_drop` → `helper_html5_drag_and_drop(col_a, col_b)` via JS event simulation → `assertEqual(col_a.text, "B")` and `assertEqual(col_b.text, "A")` | Sau khi kéo A lên B, nhãn của Khối A hiển thị "B" và nhãn của Khối B hiển thị "A", xác nhận việc hoán đổi thành công. | Cao |
| TC_DD_02 | `test_tc2_drag_b_to_a` | Phân vùng tương đương - Độ bền | Thực hiện một chu kỳ kéo và thả đầy đủ: kéo A lên B, sau đó kéo B trở lại A và xác minh cả hai khối trở về vị trí ban đầu. | `helper_html5_drag_and_drop(col_a, col_b)` → `helper_html5_drag_and_drop(col_b, col_a)` → `assertEqual(col_a.text, "A")` and `assertEqual(col_b.text, "B")` | Sau hai lần kéo, cả hai khối trở về nhãn ban đầu ("A" và "B"), xác nhận cơ chế hoán đổi có thể đảo ngược hoàn toàn. | Trung bình |

---

## Tính năng: Danh sách thả xuống
> **Tệp:** test_dropdown.py

| Mã Test Case | Tên Hàm | Kỹ thuật | Mô tả Kịch bản | Dữ liệu / Hành động | Kết quả mong đợi | Mức độ ưu tiên |
|---|---|---|---|---|---|---|
| TC_DR_01 | `test_tc1_default_placeholder` | Phân vùng tương đương - Luồng thành công | Tải trang dropdown và xác minh trạng thái mặc định: tùy chọn giữ chỗ được chọn và không thể được người dùng chọn thủ công. | `Navigate to /dropdown` → `Select(By.ID, "dropdown")` → `assertEqual(first_selected_option.text, "Please select an option")` → `assertFalse(first_option.is_enabled())` | Dropdown hiển thị 3 tùy chọn, giữ chỗ "Please select an option" được chọn mặc định và bị vô hiệu hóa để ngăn chọn lại. | Cao |
| TC_DR_02 | `test_tc2_select_option_1` | Phân vùng tương đương - Luồng thành công | Chọn "Option 1" từ dropdown theo chỉ mục và xác minh lựa chọn được phản ánh đúng. | `Navigate to /dropdown` → `Select(By.ID, "dropdown")` → `select_by_index(1)` → `assertEqual(first_selected_option.text, "Option 1")` | "Option 1" được chọn thành công và hiển thị là giá trị hiện tại của dropdown. | Cao |
| TC_DR_03 | `test_tc3_select_option_2` | Phân vùng tương đương - Luồng thành công | Chọn "Option 2" từ dropdown bằng văn bản hiển thị và xác nhận nó trở thành lựa chọn hiện tại. | `Navigate to /dropdown` → `select_by_visible_text("Option 2")` → `assertEqual(first_selected_option.text, "Option 2")` | "Option 2" được chọn thành công theo văn bản hiển thị và được hiển thị là giá trị dropdown hiện tại. | Cao |
| TC_DR_04 | `test_tc4_switch_between_options` | Phân vùng tương đương - Độ bền | Chuyển từ "Option 1" sang "Option 2" bằng lựa chọn dựa trên giá trị và xác minh dropdown phản ánh đúng sự ghi đè. | `select_by_value("1")` → `assertEqual(..., "Option 1")` → `select_by_value("2")` → `assertEqual(..., "Option 2")` | Dropdown đúng cách thay đổi từ "Option 1" sang "Option 2", chứng minh rằng chọn giá trị mới luôn ghi đè lựa chọn trước. | Trung bình |

---

## Tính năng: Nội dung động
> **Tệp:** test_dynamic_content.py

| Mã Test Case | Tên Hàm | Kỹ thuật | Mô tả Kịch bản | Dữ liệu / Hành động | Kết quả mong đợi | Mức độ ưu tiên |
|---|---|---|---|---|---|---|
| TC_DC_01 | `test_tc1_content_structure_intact` | Phân vùng tương đương - Luồng thành công | Tải trang nội dung động và xác minh luôn có đúng 3 hàng nội dung (hình ảnh + khối văn bản) được hiển thị. | `Navigate to /dynamic_content` → `find_elements(By.CSS_SELECTOR, "#content > .row:not(.large-centered)")` → `assertEqual(len(images), 3)` | Đúng 3 cặp hàng hình ảnh-văn bản hiển thị trên mỗi lần tải trang, xác nhận cấu trúc nội dung nhất quán. | Trung bình |
| TC_DC_02 | `test_tc2_content_changes_on_refresh` | Phân vùng tương đương - Độ bền | Làm mới trang tối đa 3 lần và xác minh ít nhất một số nội dung (hình ảnh hoặc văn bản) thay đổi giữa các lần tải, xác nhận ngẫu nhiên hóa đang hoạt động. | `get_content_state()` before → `driver.refresh()` up to 3× → `get_content_state()` after → `assertNotEqual(initial, refreshed)` | Ít nhất một phần tử nội dung khác nhau giữa lần tải đầu tiên và lần làm mới tiếp theo, chứng minh trang thực sự động. | Trung bình |
| TC_DC_03 | `test_tc3_static_content_parameter` | Phân vùng tương đương - Độ bền | Điều hướng với tham số truy vấn `?with_content=static` và xác minh hai hàng đầu tiên giống hệt nhau qua các lần làm mới trang. | `Navigate to /dynamic_content?with_content=static` → `get_content_state()` → `driver.refresh()` → `assertEqual(initial_images[:2], refreshed_images[:2])` | Hai hàng nội dung đầu tiên giống hệt nhau trước và sau khi làm mới khi áp dụng tham số static, xác nhận tham số hoạt động đúng. | Thấp |

---

## Tính năng: Điều khiển động
> **Tệp:** test_dynamic_controls.py

| Mã Test Case | Tên Hàm | Kỹ thuật | Mô tả Kịch bản | Dữ liệu / Hành động | Kết quả mong đợi | Mức độ ưu tiên |
|---|---|---|---|---|---|---|
| TC_DCT_01 | `test_tc1_checkbox_removal` | Phân vùng tương đương - Luồng thành công | Nhấp nút "Remove" và đợi hộp kiểm hoàn toàn biến mất khỏi trang, sau đó xác minh thông báo xác nhận. | `Navigate to /dynamic_controls` → `Click #checkbox-example > button` → `Wait for EC.staleness_of(checkbox)` → `assertEqual(msg.text, "It's gone!")` → `assertEqual(len(find_elements(By.ID,"checkbox")), 0)` | Hộp kiểm bị xóa hoàn toàn khỏi DOM và thông báo "It's gone!" được hiển thị. | Cao |
| TC_DCT_02 | `test_tc2_checkbox_addition` | Phân vùng tương đương - Luồng thành công | Xóa hộp kiểm trước, sau đó nhấp "Add" để khôi phục, xác minh DOM bao gồm lại nó và thông báo đúng được hiển thị. | `Click Remove` → `Wait for message` → `Click Add` → `Wait for EC.presence_of_element_located(By.ID, "checkbox")` → `assertEqual(msg.text, "It's back!")` | Hộp kiểm được thêm lại thành công vào trang và thông báo xác nhận "It's back!" được hiển thị. | Cao |
| TC_DCT_03 | `test_tc3_input_enable` | Phân vùng tương đương - Luồng thành công | Nhấp nút "Enable" và đợi trường nhập văn bản trở nên tương tác, sau đó xác minh thông báo xác nhận. | `Navigate to /dynamic_controls` → `assertFalse(input_field.is_enabled())` → `Click Enable button` → `Wait for EC.element_to_be_clickable(input)` → `assertEqual(msg.text, "It's enabled!")` | Trường nhập văn bản chuyển từ vô hiệu hóa sang được bật và thông báo "It's enabled!" xác nhận thay đổi trạng thái. | Cao |
| TC_DCT_04 | `test_tc4_input_disable` | Phân vùng tương đương - Luồng thành công | Bật trường nhập trước, sau đó nhấp "Disable" và đợi trường trở về trạng thái không tương tác. | `Click Enable` → `Wait for clickable` → `Click Disable` → `Wait for lambda: not input_field.is_enabled()` → `assertEqual(msg.text, "It's disabled!")` | Trường nhập chuyển trở lại trạng thái vô hiệu hóa (không tương tác) và thông báo "It's disabled!" được hiển thị. | Cao |

---

## Tính năng: Tải nội dung bất đồng bộ
> **Tệp:** test_dynamic_loading.py

| Mã Test Case | Tên Hàm | Kỹ thuật | Mô tả Kịch bản | Dữ liệu / Hành động | Kết quả mong đợi | Mức độ ưu tiên |
|---|---|---|---|---|---|---|
| TC_DL_01 | `test_hidden_element_ep_tc1` | Phân vùng tương đương - Luồng thành công | Nhấp nút Start ở Ví dụ 1, đợi thanh tải hoàn thành và xác minh thông báo "Hello World!" ẩn trở nên hiển thị. | `Navigate to /dynamic_loading/1` → `Click #start button` → `Wait for EC.invisibility_of_element_located(By.ID, "loading")` → `assertEqual(finish.text, "Hello World!")` | Văn bản "Hello World!" được hiện ra sau khi hoạt ảnh tải hoàn thành, xác nhận cơ chế hiện phần tử ẩn hoạt động. | Nghiêm trọng |
| TC_DL_02 | `test_rendered_element_ep_tc2` | Phân vùng tương đương - Luồng thành công | Nhấp nút Start ở Ví dụ 2, đợi thanh tải và xác minh phần tử được hiển thị động vào DOM với văn bản đúng. | `Navigate to /dynamic_loading/2` → `Click #start button` → `Wait for EC.invisibility_of_element_located(By.ID, "loading")` → `assertEqual(finish.text, "Hello World!")` | Phần tử "Hello World!" được đưa vào DOM và hiển thị đúng sau khi quá trình tải hoàn thành. | Nghiêm trọng |
| TC_DL_03 | `test_double_click_sad_path_tc3` | Kiểm thử âm - Độ bền | Nhấp đúp nhanh nút Start và xác minh trang phục hồi nhẹ nhàng và vẫn hiển thị kết quả đúng mà không bị hỏng. | `Navigate to /dynamic_loading/1` → `Click Start` → `Try second click immediately` → `Wait for invisibility of #loading` → `assertEqual(finish.text, "Hello World!")` | Dù nhấp đúp nhanh, trang phục hồi và hiển thị đúng "Hello World!" mà không có lỗi hoặc trạng thái hỏng. | Trung bình |
| TC_DL_04 | `test_missing_element_sad_path_tc4` | Kiểm thử âm - Luồng thất bại | Cố gắng định vị nút bằng bộ chọn CSS hoàn toàn sai và xác minh ngoại lệ timeout được đưa ra như mong đợi. | `Navigate to /dynamic_loading/1` → `WebDriverWait(driver, 10).until(EC.element_to_be_clickable(By.CSS_SELECTOR, "button#wrong-id"))` → `Catch TimeoutException` | TimeoutException được đưa ra vì bộ chọn không hợp lệ không khớp gì, xác nhận kiểm thử xác minh đúng sự hiện diện của phần tử. | Trung bình |
| TC_DL_05 | `test_short_timeout_bva_tc5` | Phân tích giá trị biên - Luồng thất bại | Sử dụng timeout 0,5 giây (xa dưới thời gian tải) để xác minh thanh tải không thể hoàn thành trong cửa sổ giới hạn đó. | `Navigate to /dynamic_loading/1` → `Click Start` → `WebDriverWait(driver, 0.5).until(EC.invisibility_of_element_located(By.ID, "loading"))` → `Catch TimeoutException` | TimeoutException được đưa ra đúng cách vì thanh tải tồn tại ngoài giới hạn 0,5 giây, xác nhận hoạt ảnh mất nhiều hơn ngưỡng tối thiểu. | Trung bình |

---

## Tính năng: Quảng cáo xuất hiện khi vào trang (Modal)
> **Tệp:** test_entry_ad.py

| Mã Test Case | Tên Hàm | Kỹ thuật | Mô tả Kịch bản | Dữ liệu / Hành động | Kết quả mong đợi | Mức độ ưu tiên |
|---|---|---|---|---|---|---|
| TC_EA_01 | `test_tc1_close_entry_ad_modal` | Phân vùng tương đương - Luồng thành công | Mở trang, xóa cookie để buộc quảng cáo xuất hiện và xác minh modal có thể được đóng thành công. | `Navigate to /entry_ad` → `delete_all_cookies()` → `driver.refresh()` → `Wait for EC.visibility_of_element_located(By.ID, "modal")` → `execute_script click .modal-footer p` → `Wait for EC.invisibility_of_element_located(By.ID, "modal")` | Modal quảng cáo xuất hiện khi tải trang và có thể được đóng thành công, biến mất khỏi khung nhìn. | Cao |
| TC_EA_02 | `test_tc2_ad_does_not_reappear_on_refresh` | Phân vùng tương đương - Độ bền | Đóng modal một lần, sau đó làm mới trang trong khi giữ cookie phiên và xác nhận quảng cáo không xuất hiện lại. | `Dismiss modal` → `driver.refresh()` → `WebDriverWait(driver, 3).until(visibility_of(By.ID, "modal"))` → `Catch exception (expected)` | Sau lần đóng đầu tiên, modal không xuất hiện lại ở lần làm mới trang tiếp theo, xác nhận cơ chế ẩn dựa trên cookie hoạt động đúng. | Cao |
| TC_EA_03 | `test_tc3_ad_reappears_on_cleared_cookies` | Phân vùng tương đương - Độ bền | Đóng modal, xóa tất cả cookie, làm mới và xác minh quảng cáo xuất hiện lại như thể đây là lần đầu người dùng truy cập. | `Dismiss modal` → `delete_all_cookies()` → `driver.refresh()` → `Wait for EC.visibility_of_element_located(By.ID, "modal")` | Modal quảng cáo xuất hiện lại sau khi cookie được xóa, xác nhận hệ thống sử dụng đúng cookie để theo dõi người dùng đã xem quảng cáo hay chưa. | Trung bình |

---

## Tính năng: Phát hiện ý định thoát trang
> **Tệp:** test_exit_intent.py

| Mã Test Case | Tên Hàm | Kỹ thuật | Mô tả Kịch bản | Dữ liệu / Hành động | Kết quả mong đợi | Mức độ ưu tiên |
|---|---|---|---|---|---|---|
| TC_EI_01 | `test_exit_intent_happy_path_tc1` | Phân vùng tương đương - Luồng thành công | Mô phỏng chuột người dùng rời khỏi khung nhìn trình duyệt, xác minh modal ý định thoát xuất hiện với tiêu đề đúng, sau đó đóng nó. | `Navigate to /exit_intent` → `execute_script: document.documentElement.dispatchEvent(new MouseEvent('mouseleave'))` → `Wait for .modal` → `assertEqual(h3.text, "THIS IS A MODAL WINDOW")` → `Click .modal-footer p` | Modal xuất hiện với tiêu đề "THIS IS A MODAL WINDOW" khi ý định thoát được kích hoạt và đóng đúng khi bị đóng. | Cao |
| TC_EI_02 | `test_exit_intent_one_time_trigger_tc2` | Phân vùng tương đương - Độ bền | Kích hoạt và đóng modal, sau đó kích hoạt ý định thoát lần thứ hai và xác minh modal không xuất hiện lại (logic một lần). | `_trigger_exit_intent()` → `Dismiss modal` → `_trigger_exit_intent()` again → `WebDriverWait(driver, 3)` → `Catch TimeoutException` | Modal đúng cách tự ẩn sau lần đóng đầu tiên và không xuất hiện lại ở lần kích hoạt ý định thoát thứ hai trong cùng phiên. | Trung bình |
| TC_EI_03 | `test_exit_intent_no_trigger_within_bounds_tc3` | Kiểm thử âm - Luồng thất bại | Di chuyển chuột trong vùng trang hợp lệ (không ra ngoài khung nhìn) và xác minh chuyển động bình thường này không kích hoạt modal ý định thoát. | `Navigate to /exit_intent` → `ActionChains.move_to_element(body).move_by_offset(100, 100).perform()` → `WebDriverWait(driver, 2)` → `Catch TimeoutException` | Di chuyển chuột trong ranh giới trang không kích hoạt modal ý định thoát, xác nhận nó chỉ được kích hoạt khi rời khỏi khung nhìn. | Trung bình |
| TC_EI_04 | `test_exit_intent_overlay_blocking_tc4` | Kiểm thử âm - Bảo mật | Kích hoạt modal ý định thoát và sau đó cố gắng nhấp vào liên kết nền qua lớp phủ modal, xác minh lớp phủ chặn tương tác đúng cách. | `_trigger_exit_intent()` → `Wait for .modal` → `footer_link.click()` → `Catch ElementClickInterceptedException` | Lớp phủ modal ngăn bất kỳ phần tử nền nào có thể nhấp trong khi đang hoạt động, xác nhận hành vi bảo mật của modal là đúng. | Cao |

---

## Tính năng: Tải xuống tệp
> **Tệp:** test_file_download.py

| Mã Test Case | Tên Hàm | Kỹ thuật | Mô tả Kịch bản | Dữ liệu / Hành động | Kết quả mong đợi | Mức độ ưu tiên |
|---|---|---|---|---|---|---|
| TC_FD_01 | `test_tc1_download_success` | Phân vùng tương đương - Luồng thành công | Nhấp vào liên kết tệp tải xuống đầu tiên và xác minh tệp thực sự xuất hiện trong thư mục tải xuống được cấu hình trên hệ thống tệp cục bộ. | `Navigate to /download` → `find_elements(By.CSS_SELECTOR, ".example a")[0].click()` → `Poll os.path.exists(file_path)` for up to 10 seconds | Tệp đã tải xuống được tìm thấy trong thư mục test_downloads trong vòng 10 giây, xác nhận tải xuống hoàn thành thành công. | Cao |

---

## Tính năng: Tải lên tệp
> **Tệp:** test_file_upload.py

| Mã Test Case | Tên Hàm | Kỹ thuật | Mô tả Kịch bản | Dữ liệu / Hành động | Kết quả mong đợi | Mức độ ưu tiên |
|---|---|---|---|---|---|---|
| TC_FU_01 | `test_tc1_upload_valid_file` | Phân vùng tương đương - Luồng thành công | Tạo tệp văn bản tạm thời, tải lên qua phần tử nhập tệp và xác minh thông báo thành công xuất hiện sau khi gửi. | `Navigate to /upload` → `Create temp file` → `find_element(By.ID, "file-upload").send_keys(file_path)` → `Click #file-submit` → `assertEqual(h3.text, "File Uploaded!")` | Tiêu đề thành công "File Uploaded!" được hiển thị sau khi gửi tệp hợp lệ, xác nhận quy trình tải lên hoạt động từ đầu đến cuối. | Cao |
| TC_FU_02 | `test_tc2_upload_empty_submission` | Kiểm thử âm - Luồng thất bại | Gửi biểu mẫu tải lên mà không chọn tệp nào và xác minh hệ thống trả về phản hồi lỗi máy chủ phù hợp. | `Navigate to /upload` → `find_element(By.ID, "file-submit").click()` (no file selected) → `assertEqual(h1.text, "Internal Server Error")` | Máy chủ trả về lỗi 500 Internal Server Error khi không có tệp nào được đính kèm vào lần gửi tải lên, xác nhận điểm cuối xác nhận sự hiện diện của tệp. | Cao |

---

## Tính năng: Menu nổi (luôn hiển thị khi cuộn)
> **Tệp:** test_floating_menu.py

| Mã Test Case | Tên Hàm | Kỹ thuật | Mô tả Kịch bản | Dữ liệu / Hành động | Kết quả mong đợi | Mức độ ưu tiên |
|---|---|---|---|---|---|---|
| TC_FM_01 | `test_tc1_menu_visible_top` | Phân vùng tương đương - Luồng thành công | Tải trang menu nổi và xác minh menu điều hướng hiển thị ở đầu mà không cần cuộn. | `Navigate to /floating_menu` → `Wait for EC.visibility_of_element_located(By.ID, "menu")` → `assertTrue(menu.is_displayed())` | Menu điều hướng nổi hiển thị ngay sau khi tải trang, trước bất kỳ tương tác người dùng nào. | Trung bình |
| TC_FM_02 | `test_tc2_menu_visible_on_scroll` | Phân vùng tương đương - Độ bền | Cuộn trang đến tận cùng và xác minh menu nổi vẫn hiển thị và các liên kết của nó vẫn có thể truy cập. | `Navigate to /floating_menu` → `execute_script("window.scrollTo(0, document.body.scrollHeight)")` → `assertTrue(menu.is_displayed())` → `assertTrue(home_link.is_displayed() and about_link.is_displayed())` | Menu nổi vẫn hiển thị và các liên kết của nó (Home, About) vẫn được hiển thị ngay cả khi trang được cuộn đến tận cùng. | Cao |
| TC_FM_03 | `test_tc3_menu_anchor_links_work` | Phân vùng tương đương - Luồng thành công | Nhấp vào liên kết "Home" trong menu nổi và xác minh URL trang được cập nhật với đúng đoạn neo. | `Navigate to /floating_menu` → `Wait for EC.element_to_be_clickable(By.LINK_TEXT, "Home")` → `click()` → `assertIn("#home", driver.current_url)` | Nhấp vào liên kết "Home" cập nhật URL để bao gồm đoạn "#home", xác nhận điều hướng neo hoạt động. | Trung bình |

---

## Tính năng: Quên mật khẩu
> **Tệp:** test_forgot_password.py

| Mã Test Case | Tên Hàm | Kỹ thuật | Mô tả Kịch bản | Dữ liệu / Hành động | Kết quả mong đợi | Mức độ ưu tiên |
|---|---|---|---|---|---|---|
| TC_FP_01 | `test_tc1_valid_email_submission` | Phân vùng tương đương - Luồng thành công | Gửi địa chỉ email được định dạng đúng tới biểu mẫu Quên mật khẩu và xác minh hệ thống xử lý yêu cầu mà không bị sập bất ngờ. | `Navigate to /forgot_password` → `find_element(By.ID, "email").send_keys("test_user_valid@example.com")` → `Click #form_submit` → `Wait for page navigation` | Hệ thống hoặc hiển thị thông báo thành công hoặc trả về lỗi 500 đã biết từ điểm cuối demo này, nhưng không bị sập bất ngờ. | Trung bình |
| TC_FP_02 | `test_tc2_empty_email_submission` | Kiểm thử âm - Luồng thất bại | Gửi biểu mẫu với trường email hoàn toàn trống và xác minh máy chủ trả về phản hồi lỗi. | `Navigate to /forgot_password` → `Click #form_submit` (no email entered) → `assertIn("Internal Server Error", result_text)` | "Internal Server Error" được trả về cho lần gửi trống, xác nhận điểm cuối xác nhận sự hiện diện của trường email. | Trung bình |
| TC_FP_03 | `test_tc3_invalid_email_format` | Kiểm thử âm - Luồng thất bại | Nhập chuỗi không đúng định dạng (không có "@" hoặc miền) làm email và xác minh hệ thống phản hồi bằng lỗi thay vì thành công. | `Navigate to /forgot_password` → `send_keys("user_without_at_symbol_or_domain")` → `Click #form_submit` → `assertTrue("Internal Server Error" in result or "Your e-mail's been sent!" in result)` | Email không đúng định dạng được xử lý mà không bị sập bất ngờ, trả về lỗi máy chủ hoặc thông báo thành công demo đã biết. | Thấp |

---

## Tính năng: Đăng nhập qua biểu mẫu
> **Tệp:** test_form_authentication.py

| Mã Test Case | Tên Hàm | Kỹ thuật | Mô tả Kịch bản | Dữ liệu / Hành động | Kết quả mong đợi | Mức độ ưu tiên |
|---|---|---|---|---|---|---|
| TC_FA_01 | `test_tc1_login_success` | Phân vùng tương đương - Luồng thành công | Đăng nhập với thông tin xác thực hoàn toàn hợp lệ và xác minh người dùng được chuyển hướng đến vùng bảo mật với thông báo flash thành công. | `Navigate to /login` → `send_keys("tomsmith") to #username` → `send_keys("SuperSecretPassword!") to #password` → `Click button[type='submit']` → `assertIn("/secure", current_url)` → `assertIn("You logged into a secure area!", flash)` | Người dùng được chuyển hướng đến `/secure` và thông báo flash "You logged into a secure area!" được hiển thị. | Nghiêm trọng |
| TC_FA_02 | `test_tc2_invalid_password` | Kiểm thử âm - Luồng thất bại | Thử đăng nhập với tên người dùng đúng nhưng mật khẩu sai và xác minh thông báo flash lỗi phù hợp được hiển thị. | `helper_login("tomsmith", "wrongpassword")` → `assertIn("Your password is invalid!", get_flash_msg())` | Thông báo flash "Your password is invalid!" được hiển thị và người dùng ở lại trang đăng nhập. | Nghiêm trọng |
| TC_FA_03 | `test_tc3_invalid_username` | Kiểm thử âm - Luồng thất bại | Thử đăng nhập với tên người dùng không tồn tại và xác minh hệ thống trả về lỗi tên người dùng đúng. | `helper_login("wronguser", "SuperSecretPassword!")` → `assertIn("Your username is invalid!", get_flash_msg())` | Thông báo flash "Your username is invalid!" được hiển thị, xác nhận hệ thống xác thực sự tồn tại của tên người dùng trước. | Nghiêm trọng |
| TC_FA_04 | `test_tc4_empty_credentials` | Kiểm thử âm - Luồng thất bại | Gửi biểu mẫu đăng nhập với cả hai trường tên người dùng và mật khẩu hoàn toàn trống. | `helper_login("", "")` → `assertIn("Your username is invalid!", get_flash_msg())` | Hệ thống từ chối đúng cách lần gửi trống và hiển thị thông báo lỗi "Your username is invalid!". | Cao |
| TC_FA_05 | `test_tc5_empty_password` | Kiểm thử âm - Luồng thất bại | Cung cấp tên người dùng hợp lệ nhưng để trường mật khẩu hoàn toàn trống, sau đó gửi. | `helper_login("tomsmith", "")` → `assertIn("Your password is invalid!", get_flash_msg())` | Thông báo flash "Your password is invalid!" được hiển thị, xác nhận hệ thống xác thực cả hai trường độc lập. | Cao |
| TC_FA_06 | `test_tc6_empty_username` | Kiểm thử âm - Luồng thất bại | Để trống trường tên người dùng trong khi cung cấp mật khẩu đúng, sau đó gửi. | `helper_login("", "SuperSecretPassword!")` → `assertIn("Your username is invalid!", get_flash_msg())` | Thông báo "Your username is invalid!" xuất hiện, xác nhận tên người dùng được xác thực trước mật khẩu. | Cao |
| TC_FA_07 | `test_tc7_logout_functionality` | Phân vùng tương đương - Luồng thành công | Đăng nhập thành công, sau đó nhấp nút đăng xuất và xác minh người dùng được chuyển hướng trở lại trang đăng nhập với thông báo xác nhận đăng xuất. | `helper_login("tomsmith", "SuperSecretPassword!")` → `Click a.button.secondary` → `Wait for EC.url_contains("/login")` → `assertIn("You logged out of the secure area!", flash)` | Người dùng được chuyển hướng đến `/login` và thông báo flash "You logged out of the secure area!" xác nhận đăng xuất thành công. | Nghiêm trọng |
| TC_FA_08 | `test_tc8_case_sensitive_username` | Kiểm thử âm - Trường hợp biên | Thử đăng nhập với tên người dùng dùng chữ hoa/thường sai (ví dụ: "TomSmith") để xác minh phân biệt chữ hoa/thường. | `helper_login("TomSmith", "SuperSecretPassword!")` → `assertIn("Your username is invalid!", get_flash_msg())` | Xác thực thất bại với tên người dùng viết hoa sai, xác nhận hệ thống phân biệt chữ hoa/thường cho tên người dùng. | Trung bình |
| TC_FA_09 | `test_tc9_case_sensitive_password` | Kiểm thử âm - Trường hợp biên | Thử đăng nhập với mật khẩu toàn chữ thường để xác minh trường mật khẩu phân biệt chữ hoa/thường. | `helper_login("tomsmith", "supersecretpassword!")` → `assertIn("Your password is invalid!", get_flash_msg())` | Xác thực thất bại với mật khẩu toàn chữ thường, xác nhận hệ thống phân biệt chữ hoa/thường cho mật khẩu. | Trung bình |
| TC_FA_10 | `test_tc10_special_characters` | Kiểm thử bảo mật - Độ bền | Nhập tên người dùng được tạo hoàn toàn từ ký tự đặc biệt và xác minh hệ thống từ chối an toàn mà không bị sập. | `helper_login("!@#$%^&*", "SuperSecretPassword!")` → `assertIn("Your username is invalid!", get_flash_msg())` | Tên người dùng ký tự đặc biệt bị từ chối với thông báo tên người dùng không hợp lệ tiêu chuẩn, xác nhận không có lỗ hổng injection. | Trung bình |


---

## Tính năng: Khung nhúng (iFrame & Frames)
> **Tệp:** test_frame.py

| Mã Test Case | Tên Hàm | Kỹ thuật | Mô tả Kịch bản | Dữ liệu / Hành động | Kết quả mong đợi | Mức độ ưu tiên |
|---|---|---|---|---|---|---|
| TC_IF_01 | `test_iframe_happy_path_tc1` | Phân vùng tương đương - Luồng thành công | Switch the browser context into the TinyMCE iFrame, inject text into the editor, and verify the content is correctly written. | `Navigate to /iframe` → `Wait for EC.frame_to_be_available_and_switch_to_it(By.ID, "mce_0_ifr")` → `execute_script set innerText on #tinymce` → `assertEqual(editor.text, "Happy Path Test")` | The text "Happy Path Test" is successfully written into the iFrame's editor and confirmed by reading back the element's text. | Cao |
| TC_IF_02 | `test_nested_frames_happy_path_tc2` | Phân vùng tương đương - Luồng thành công | Navigate through two levels of nested frames (root → frame-top → frame-middle) and verify the correct content is found in the deepest frame. | `Navigate to /nested_frames` → `switch_to.frame("frame-top")` → `switch_to.frame("frame-middle")` → `assertEqual(content.text.strip(), "MIDDLE")` | The text "MIDDLE" is correctly found inside the deepest targeted frame, confirming the multi-level frame traversal works correctly. | Cao |
| TC_IF_03 | `test_frame_context_leak_sad_path_tc3` | Kiểm thử âm - Luồng thất bại | After switching into an iFrame, attempt to find a main-page element and verify the browser context is correctly isolated within the frame. | `switch_to.frame("mce_0_ifr")` → `try find_element(By.TAG_NAME, "h3")` → `Catch NoSuchElementException` | A NoSuchElementException is raised, confirming the driver's context is correctly locked inside the iFrame and cannot see the main document's elements. | Cao |
| TC_IF_04 | `test_invalid_frame_access_sad_path_tc4` | Kiểm thử âm - Luồng thất bại | Attempt to switch to a frame using a completely fictitious frame ID and verify the appropriate exception is raised. | `Navigate to /iframe` → `driver.switch_to.frame("ghost_frame_99")` → `Catch NoSuchFrameException` | A NoSuchFrameException is raised, confirming the WebDriver correctly validates frame IDs and rejects invalid ones. | Trung bình |
| TC_IF_05 | `test_sibling_frame_isolation_sad_path_tc5` | Kiểm thử âm - Luồng thất bại | From inside "frame-left", attempt to jump directly to the sibling "frame-right" without returning to the parent context first. | `switch_to.frame("frame-top")` → `switch_to.frame("frame-left")` → `try switch_to.frame("frame-right")` → `Catch NoSuchFrameException` | A NoSuchFrameException is raised, confirming that direct sibling-to-sibling frame navigation is not allowed and requires returning to a parent context first. | Trung bình |

---

## Tính năng: Định vị địa lý
> **Tệp:** test_geolocation.py

| Mã Test Case | Tên Hàm | Kỹ thuật | Mô tả Kịch bản | Dữ liệu / Hành động | Kết quả mong đợi | Mức độ ưu tiên |
|---|---|---|---|---|---|---|
| TC_GEO_01 | `test_tc1_geolocation_reveal_coordinates` | Phân vùng tương đương - Luồng thành công | Click the "Where am I?" button with a mocked GPS location (Hanoi, Vietnam) and verify the latitude and longitude values are displayed as valid numbers. | `CDP: Emulation.setGeolocationOverride (lat:21.0285, long:105.8542)` → `Click .example button` → `Wait for #lat-value` and `#long-value` → `float(lat.text)` | Valid floating-point numbers for latitude and longitude are displayed on the page, confirming the geolocation feature works with the mocked coordinates. | Cao |
| TC_GEO_02 | `test_tc2_geolocation_map_link` | Phân vùng tương đương - Luồng thành công | After triggering geolocation, verify that a Google Maps link appears with the correct latitude value embedded in the URL. | `Click .example button` → `Wait for #map-link a` → `href = get_attribute("href")` → `assertIn("google", href)` → `assertIn(lat, href)` | A Google Maps link is generated containing the word "google" and the exact mocked latitude value, confirming the dynamic URL construction works correctly. | Trung bình |

---

## Tính năng: Thanh trượt ngang
> **Tệp:** test_horizontal_slider.py

| Mã Test Case | Tên Hàm | Kỹ thuật | Mô tả Kịch bản | Dữ liệu / Hành động | Kết quả mong đợi | Mức độ ưu tiên |
|---|---|---|---|---|---|---|
| TC_HS_01 | `test_tc1_slider_increments_correctly` | Phân vùng tương đương - Luồng thành công | Click on the slider and press the right arrow key once, then verify the slider value has incremented by exactly 0.5. | `Navigate to /horizontal_slider` → `Click input[type='range']` → `send_keys(Keys.ARROW_RIGHT)` → `assertEqual(new_value, initial_value + 0.5)` | The slider value increases by exactly 0.5 after pressing the right arrow key once, confirming the step increment is correctly configured. | Trung bình |
| TC_HS_02 | `test_tc2_slider_boundary_min` | Phân tích giá trị biên - Luồng thất bại | Press the left arrow key 15 times on the slider to push it past the minimum possible value and verify it does not go below 0. | `Click input[type='range']` → `send_keys(Keys.ARROW_LEFT) × 15` → `assertEqual(range.text, "0")` | The slider stops at 0 and does not go below the minimum boundary, regardless of how many times the left arrow is pressed. | Trung bình |

---

## Tính năng: Hiệu ứng di chuột (Hover)
> **Tệp:** test_hovers.py

| Mã Test Case | Tên Hàm | Kỹ thuật | Mô tả Kịch bản | Dữ liệu / Hành động | Kết quả mong đợi | Mức độ ưu tiên |
|---|---|---|---|---|---|---|
| TC_HV_01 | `test_tc1_hover_user1` | Phân vùng tương đương - Luồng thành công | Hover over the first user profile image and verify the hidden caption reveals the correct username "user1". | `Navigate to /hovers` → `find_elements(By.CLASS_NAME, "figure")[0]` → `ActionChains.move_to_element()` → `JS: caption style opacity=1` → `assertEqual(caption_header.text, "name: user1")` | The caption "name: user1" appears when hovering over the first profile image, confirming the hover reveal works. | Trung bình |
| TC_HV_02 | `test_tc2_hover_user2` | Phân vùng tương đương - Luồng thành công | Hover over the second user profile image and verify the caption reveals "user2". | `figures[1]` → `move_to_element()` → `JS force opacity` → `assertEqual(caption_header.text, "name: user2")` | The caption "name: user2" appears on hover over the second image, confirming each image maps to the correct user. | Trung bình |
| TC_HV_03 | `test_tc3_hover_user3` | Phân vùng tương đương - Luồng thành công | Hover over the third user profile image and verify the caption reveals "user3". | `figures[2]` → `move_to_element()` → `JS force opacity` → `assertEqual(caption_header.text, "name: user3")` | The caption "name: user3" appears on hover over the third image, completing the verification of all three profile figures. | Trung bình |

---

## Tính năng: Cuộn vô hạn
> **Tệp:** test_infinite_scroll.py

| Mã Test Case | Tên Hàm | Kỹ thuật | Mô tả Kịch bản | Dữ liệu / Hành động | Kết quả mong đợi | Mức độ ưu tiên |
|---|---|---|---|---|---|---|
| TC_IS_01 | `test_tc1_initial_content_load` | Phân vùng tương đương - Luồng thành công | Load the infinite scroll page and verify at least one content block is present immediately without any scrolling. | `Navigate to /infinite_scroll` → `Wait for EC.presence_of_element_located(By.CLASS_NAME, "jscroll-added")` → `assertGreaterEqual(count, 1)` | At least one paragraph content block is visible on the initial page load, confirming the page's default content renders correctly. | Trung bình |
| TC_IS_02 | `test_tc2_scroll_loads_more_content` | Phân vùng tương đương - Độ bền | Scroll to the bottom of the page three times and verify that new content is appended each time, confirming the infinite scroll mechanism is active. | `get_paragraph_count() before` → `Loop 3×: execute_script("window.scrollTo(0, document.body.scrollHeight)")` → `time.sleep(1.5)` → `assertGreater(final_count, initial_count)` | The total number of content blocks increases after scrolling, confirming new content is dynamically loaded via AJAX as the user scrolls down. | Cao |

---

## Tính năng: Trường nhập số
> **Tệp:** test_inputs.py

| Mã Test Case | Tên Hàm | Kỹ thuật | Mô tả Kịch bản | Dữ liệu / Hành động | Kết quả mong đợi | Mức độ ưu tiên |
|---|---|---|---|---|---|---|
| TC_NI_01 | `test_tc1_valid_number_input` | Phân vùng tương đương - Luồng thành công | Type valid positive and negative integers into the number input field and verify the values are accepted and stored correctly. | `Navigate to /inputs` → `send_keys("500")` → `assertEqual(value, "500")` → `clear()` → `send_keys("-35")` → `assertEqual(value, "-35")` | Both "500" and "-35" are accepted by the number field and their values are correctly reflected in the input element. | Trung bình |
| TC_NI_02 | `test_tc2_arrow_up_increment` | Phân vùng tương đương - Luồng thành công | Type a starting value of 10, then press the up arrow key and verify the value increments by exactly 1. | `send_keys("10")` → `send_keys(Keys.ARROW_UP)` → `assertEqual(value, "11")` | The value increments from 10 to 11 after one up-arrow press, confirming the step increment is correctly set to 1. | Trung bình |
| TC_NI_03 | `test_tc3_arrow_down_decrement` | Phân vùng tương đương - Luồng thành công | Type a starting value of 10, then press the down arrow key and verify the value decrements by exactly 1. | `send_keys("10")` → `send_keys(Keys.ARROW_DOWN)` → `assertEqual(value, "9")` | The value decrements from 10 to 9 after one down-arrow press, confirming the decrement step is correctly set to 1. | Trung bình |
| TC_NI_04 | `test_tc4_invalid_text_input` | Kiểm thử âm - Luồng thất bại | Type alphabetical letters into a number-only input field and verify the field correctly rejects non-numeric input. | `send_keys("abc")` → `assertEqual(input.get_attribute("value"), "")` | The number input field ignores all alphabetical characters, leaving the value empty, confirming the browser-level type validation is working. | Cao |

---

## Tính năng: Trang có lỗi JavaScript
> **Tệp:** test_javascript_error.py

| Mã Test Case | Tên Hàm | Kỹ thuật | Mô tả Kịch bản | Dữ liệu / Hành động | Kết quả mong đợi | Mức độ ưu tiên |
|---|---|---|---|---|---|---|
| TC_JSE_01 | `test_javascript_error_page_loads_tc1` | Phân vùng tương đương - Luồng thành công | Navigate to the JavaScript error page and verify the informational paragraph is visible despite the JS error firing on load. | `Navigate to /javascript_error` → `Wait for EC.presence_of_element_located(By.TAG_NAME, "p")` → `assertIn("JavaScript error", content.text)` | The page loads and the content paragraph containing "JavaScript error" is visible, confirming the page renders despite the JS error in the onload handler. | Trung bình |
| TC_JSE_02 | `test_javascript_error_console_log_tc2` | Phân vùng tương đương - Độ bền | After loading the page, use JavaScript execution to confirm the known broken property access returns "undefined" and the error-triggering function exists in scope. | `execute_script("return typeof document.propertyThatDoesNotExist")` → `assertEqual(result, "undefined")` → `execute_script("return typeof window.loadError")` → `assertEqual(fn_type, "function")` | The broken property is correctly identified as "undefined" and the `loadError` function is confirmed to exist in the page's global scope. | Trung bình |
| TC_JSE_03 | `test_javascript_error_no_heading_tc3` | Kiểm thử âm - Cấu trúc | Confirm that this specific page intentionally has no `<h3>` heading element, distinguishing it from other pages in the suite. | `Navigate to /javascript_error` → `find_elements(By.TAG_NAME, "h3")` → `assertEqual(len(h3_elements), 0)` | No `<h3>` elements are found, confirming the page structure is a bare `<p>` inside `<body>` without the standard heading wrapper. | Thấp |
| TC_JSE_04 | `test_javascript_error_page_title_tc4` | Phân vùng tương đương - Trường hợp biên | Verify the browser tab title of the JavaScript error page is the correct, unique title rather than the generic site title. | `Navigate to /javascript_error` → `driver.title` → `assertIn("JavaScript error", title)` | The page title contains "JavaScript error", confirming the browser is on the correct page and not on the generic "The Internet" homepage. | Thấp |

---

## Tính năng: Menu jQuery UI
> **Tệp:** test_jquery_ui_menus.py

| Mã Test Case | Tên Hàm | Kỹ thuật | Mô tả Kịch bản | Dữ liệu / Hành động | Kết quả mong đợi | Mức độ ưu tiên |
|---|---|---|---|---|---|---|
| TC_JQM_01 | `test_jquery_menu_hover_pdf_tc1` | Phân vùng tương đương - Luồng thành công | Expand the nested "Enabled → Downloads" menu hierarchy and verify the PDF download link is accessible with a correct href. | `Navigate to /jqueryui/menu` → `JS: force show Enabled submenu` → `JS: force show Downloads submenu` → `find_element(By.LINK_TEXT, "PDF")` → `assertIn("pdf", pdf_href.lower())` | The PDF link is found in the nested submenu and its href attribute contains "pdf", confirming the multi-level menu hierarchy is accessible. | Cao |
| TC_JQM_02 | `test_jquery_menu_hover_excel_tc2` | Phân vùng tương đương - Luồng thành công | Expand the "Enabled → Downloads" menu and verify the Excel download link is accessible with an "xls" href. | `Navigate to /jqueryui/menu` → `JS: force show Enabled submenu` → `JS: force show Downloads submenu` → `find_element(By.LINK_TEXT, "Excel")` → `assertIn("xls", excel_href.lower())` | The Excel link is found in the nested submenu and its href contains "xls", confirming all three nested download links are correctly wired. | Trung bình |
| TC_JQM_03 | `test_jquery_menu_disabled_not_clickable_tc3` | Kiểm thử âm - Luồng thất bại | Verify that clicking the "Disabled" top-level menu item does not navigate the user away from the current page. | `find_element(XPath //li[contains(@class,'ui-state-disabled')]/a)` → `assertIn("ui-state-disabled", classes)` → `disabled_item.click()` → `assertEqual(url_after_base, url_before_base)` | The URL remains unchanged after clicking the disabled item, confirming the jQuery UI disabled state correctly prevents navigation. | Cao |
| TC_JQM_04 | `test_jquery_menu_disabled_no_submenu_tc4` | Kiểm thử âm - Luồng thất bại | Confirm the "Disabled" menu item has no visible or accessible sub-menus hidden beneath it. | `find_element(XPath //li[contains(@class,'ui-state-disabled')])` → `disabled_li.find_elements(By.TAG_NAME, "ul")` → `For each ul: assertFalse(is_displayed())` | Any child `<ul>` elements within the disabled menu item are confirmed to be hidden and not displayed to the user. | Trung bình |

---

## Tính năng: Hộp thoại JavaScript (Alert/Confirm)
> **Tệp:** test_js_alerts.py

| Mã Test Case | Tên Hàm | Kỹ thuật | Mô tả Kịch bản | Dữ liệu / Hành động | Kết quả mong đợi | Mức độ ưu tiên |
|---|---|---|---|---|---|---|
| TC_JSA_01 | `test_tc1_accept_js_alert` | Phân vùng tương đương - Luồng thành công | Click the "JS Alert" button, verify the alert text, accept it, and confirm the result message updates correctly. | `Navigate to /javascript_alerts` → `Click button[onclick='jsAlert()']` → `Wait for EC.alert_is_present()` → `assertEqual(alert.text, "I am a JS Alert")` → `alert.accept()` → `assertEqual(result, "You successfully clicked an alert")` | The JS Alert shows the correct text, is dismissed successfully, and the page displays "You successfully clicked an alert". | Cao |
| TC_JSA_02 | `test_tc2_accept_js_confirm` | Phân vùng tương đương - Luồng thành công | Click the "JS Confirm" button, accept the confirmation dialog, and verify the result message shows "Ok" was clicked. | `Click button[onclick='jsConfirm()']` → `alert.accept()` → `assertEqual(result, "You clicked: Ok")` | After accepting the confirmation dialog, the result message "You clicked: Ok" is displayed, confirming the accept action is registered. | Cao |
| TC_JSA_03 | `test_tc3_dismiss_js_confirm` | Kiểm thử âm - Luồng thất bại | Click the "JS Confirm" button, dismiss (cancel) the dialog, and verify the result message shows "Cancel" was clicked. | `Click button[onclick='jsConfirm()']` → `alert.dismiss()` → `assertEqual(result, "You clicked: Cancel")` | After dismissing the confirmation dialog, the result message "You clicked: Cancel" is displayed, confirming the cancel action is correctly handled. | Cao |

---

## Tính năng: Nhận diện phím bấm
> **Tệp:** test_key_presses.py

| Mã Test Case | Tên Hàm | Kỹ thuật | Mô tả Kịch bản | Dữ liệu / Hành động | Kết quả mong đợi | Mức độ ưu tiên |
|---|---|---|---|---|---|---|
| TC_KP_01 | `test_tc1_special_keyboard_keys` | Phân vùng tương đương - Luồng thành công | Press a series of special non-alphanumeric keys (Space, Enter, Tab, Escape, Backspace, Alt) and verify the page correctly identifies and displays each one. | `Navigate to /key_presses` → `ActionChains.send_keys(Keys.SPACE)` ... `Keys.ALT` → `For each: assertEqual(result, "You entered: {KEYNAME}")` | Each special key is correctly identified by name (e.g., "SPACE", "ENTER", "TAB") and displayed in the result section. | Trung bình |
| TC_KP_02 | `test_tc2_alphanumeric_keyboard_keys` | Phân vùng tương đương - Luồng thành công | Press basic printable characters (a, Z, 7, @) and verify the page echoes back the correct representation for each. | `ActionChains.send_keys("a")` → `assertEqual("You entered: A")` → `send_keys("Z")` → `assertEqual("You entered: Z")` → `send_keys("7")` → `assertEqual("You entered: 7")` | Alphanumeric keys are correctly echoed back in uppercase format; special symbols like "@" are echoed with their ASCII name. | Trung bình |

---

## Tính năng: DOM lớn và sâu
> **Tệp:** test_large_deep_dom.py

| Mã Test Case | Tên Hàm | Kỹ thuật | Mô tả Kịch bản | Dữ liệu / Hành động | Kết quả mong đợi | Mức độ ưu tiên |
|---|---|---|---|---|---|---|
| TC_LDD_01 | `test_large_dom_deep_sibling_tc1` | Phân vùng tương đương - Luồng thành công | Navigate to the large DOM page and locate a deeply nested sibling element by its exact ID, verifying the correct text content. | `Navigate to /large` → `find_element(By.ID, "sibling-2.2")` → `assertIn("2.2", text)` | The element with ID "sibling-2.2" is found and contains the text "2.2", confirming deep DOM traversal works at scale. | Trung bình |
| TC_LDD_02 | `test_large_dom_boundary_cell_tc2` | Phân tích giá trị biên - Luồng thành công | Use JavaScript to discover all sibling elements, sort them numerically, and verify the highest-indexed (BVA-max) boundary element exists with content. | `execute_script: Array.from(document.querySelectorAll('[id^="sibling-"]'))` → `Sort numerically` → `find_element(By.ID, boundary_id)` → `assertTrue(len(text) > 0)` | The boundary element at the largest sibling index is found and has non-empty text, confirming the DOM is fully rendered even at its deepest point. | Trung bình |
| TC_LDD_03 | `test_large_dom_invalid_id_sad_path_tc3` | Kiểm thử âm - Luồng thất bại | Attempt to locate a completely non-existent element ID in the large DOM and verify a timeout is raised gracefully. | `WebDriverWait(driver, 2).until(EC.presence_of_element_located(By.ID, "large-999-999"))` → `Catch TimeoutException` | A TimeoutException is raised, confirming the element does not exist and the test framework handles the absence gracefully. | Thấp |
| TC_LDD_04 | `test_large_dom_invalid_xpath_sad_path_tc4` | Kiểm thử âm - Luồng thất bại | Attempt to locate a non-existent element using an invalid XPath expression and verify the timeout is raised correctly. | `WebDriverWait(driver, 2).until(EC.presence_of_element_located(By.XPATH, "//div[@id='sibling-999.999']"))` → `Catch TimeoutException` | A TimeoutException is raised, confirming the XPath query correctly returns no results for the non-existent element. | Thấp |

---

## Tính năng: Nhiều cửa sổ trình duyệt
> **Tệp:** test_multiple_windows.py

| Mã Test Case | Tên Hàm | Kỹ thuật | Mô tả Kịch bản | Dữ liệu / Hành động | Kết quả mong đợi | Mức độ ưu tiên |
|---|---|---|---|---|---|---|
| TC_MW_01 | `test_multiple_windows_switch_happy_path_tc1` | Phân vùng tương đương - Luồng thành công | Click a link that opens a new browser tab, switch the driver's context to the new tab, verify its content, close it, and return to the original tab. | `Navigate to /windows` → `Click "Click Here"` → `Wait for EC.number_of_windows_to_be(2)` → `switch_to.window(new_handle)` → `assertEqual(h3.text, "New Window")` → `close()` → `switch_to.window(original)` | The new window contains the heading "New Window". After closing it and switching back, the original window is still accessible and functional. | Cao |
| TC_MW_02 | `test_multiple_windows_isolation_sad_path_tc2` | Kiểm thử âm - Luồng thất bại | Open a new window but do NOT switch context, then attempt to read content from the new window without switching and verify the driver cannot see it. | `Click "Click Here"` → `Wait for 2 windows` → `try find_element(XPath //h3[text()='New Window'])` → `Catch NoSuchElementException` | A NoSuchElementException is raised, confirming the driver's context is strictly isolated to its current window handle. | Cao |
| TC_MW_03 | `test_invalid_window_handle_sad_path_tc3` | Kiểm thử âm - Luồng thất bại | Attempt to switch the driver to a completely fictitious window handle string and verify the correct exception is raised. | `driver.switch_to.window("ghost_tab_999")` → `Catch NoSuchWindowException` | A NoSuchWindowException is raised, confirming the WebDriver validates window handles and rejects invalid ones. | Trung bình |

---

## Tính năng: Khung lồng nhau (Nested Frames)
> **Tệp:** test_nested_frames.py

| Mã Test Case | Tên Hàm | Kỹ thuật | Mô tả Kịch bản | Dữ liệu / Hành động | Kết quả mong đợi | Mức độ ưu tiên |
|---|---|---|---|---|---|---|
| TC_NF_01 | `test_nested_frames_top_traversal_tc1` | Phân vùng tương đương - Luồng thành công | Traverse all three sibling frames within the top frame (LEFT, MIDDLE, RIGHT) sequentially and verify each contains the correct text content. | `Navigate to /nested_frames` → `switch_to.frame("frame-top")` → `switch_to.frame("frame-left")` → `assertEqual(body.text, "LEFT")` → `switch_to.parent_frame()` → `switch_to.frame("frame-middle")` → `assertEqual(content.text, "MIDDLE")` → ... RIGHT | Each of the three child frames (LEFT, MIDDLE, RIGHT) is accessed in order and contains the correct single-word text label. | Cao |
| TC_NF_02 | `test_nested_frames_bottom_traversal_tc2` | Phân vùng tương đương - Luồng thành công | Navigate from the root context directly into the bottom frame and verify it contains the text "BOTTOM". | `switch_to.default_content()` → `switch_to.frame("frame-bottom")` → `assertEqual(body.text, "BOTTOM")` | The bottom frame is accessible directly from the root context and contains the text "BOTTOM". | Trung bình |
| TC_NF_03 | `test_nested_frames_sibling_isolation_tc3` | Kiểm thử âm - Luồng thất bại | From inside "frame-left", attempt a direct jump to the sibling "frame-right" and verify this illegal navigation is blocked. | `switch_to.frame("frame-top")` → `switch_to.frame("frame-left")` → `try switch_to.frame("frame-right")` → `Catch NoSuchFrameException` | A NoSuchFrameException is raised, confirming you cannot jump directly between sibling frames without first returning to the parent context. | Trung bình |

---

## Tính năng: Thông báo flash
> **Tệp:** test_notification_messages.py

| Mã Test Case | Tên Hàm | Kỹ thuật | Mô tả Kịch bản | Dữ liệu / Hành động | Kết quả mong đợi | Mức độ ưu tiên |
|---|---|---|---|---|---|---|
| TC_NM_01 | `test_notification_single_click_ep_tc1` | Phân vùng tương đương - Luồng thành công | Click the notification trigger link once and verify the flash message displayed is one of the two known valid server responses. | `Navigate to /notification_message` → `Click "Click here"` → `Wait for #flash` → `assertIn(flash_text, VALID_MESSAGES)` | The flash message is one of the two recognized responses ("Action successful" or "Action unsuccessful, please try again"), confirming the notification system is functional. | Cao |
| TC_NM_02 | `test_notification_multi_click_ep_tc2` | Phân vùng tương đương - Độ bền | Click the notification trigger link 5 times in sequence and verify each click produces a valid flash message response. | `Loop 5×: Navigate to /notification_message` → `Click "Click here"` → `assertIn(flash_text, VALID_MESSAGES)` | All 5 clicks produce a valid flash message, confirming the notification system is stable and consistent across repeated interactions. | Trung bình |
| TC_NM_03 | `test_notification_no_unexpected_message_tc3` | Kiểm thử âm - Luồng thất bại | Click the notification link and verify the flash message is never empty and is always one of the two known server-defined messages. | `Click "Click here"` → `assertTrue(len(flash_text) > 0)` → `assertIn(flash_text, VALID_MESSAGES)` | The flash message is non-empty and matches one of the two known valid messages, confirming no unexpected or unknown responses are returned. | Trung bình |
| TC_NM_04 | `test_notification_direct_render_robustness_tc4` | Phân vùng tương đương - Độ bền | Follow the full click-to-redirect flow and confirm the final rendered URL is the expected notification-rendered endpoint with a valid flash message. | `Navigate to /notification_message` → `Click "Click here"` → `Wait for EC.url_contains("notification_message_rendered")` → `assertIn(flash_text, VALID_MESSAGES)` | After the click and redirect, the URL contains "notification_message_rendered" and the flash message on the destination page is valid. | Trung bình |


---

## Tính năng: Liên kết chuyển hướng
> **Tệp:** test_redirect_link.py

| Mã Test Case | Tên Hàm | Kỹ thuật | Mô tả Kịch bản | Dữ liệu / Hành động | Kết quả mong đợi | Mức độ ưu tiên |
|---|---|---|---|---|---|---|
| TC_RL_01 | `test_redirect_link_url_change_tc1` | Phân vùng tương đương - Luồng thành công | Click the redirect link on the redirector page and verify the browser URL changes to the expected destination page. | `Navigate to /redirector` → `Click CSS a[href='redirect']` → `Wait for EC.url_contains("status_codes")` → `assertNotEqual(url_before, url_after)` → `assertEqual(url_after, /status_codes)` | The URL changes from `/redirector` to the expected `/status_codes` destination, confirming the redirect mechanism is functional. | Cao |
| TC_RL_02 | `test_redirect_link_destination_content_tc2` | Phân vùng tương đương - Luồng thành công | Follow the redirect and verify the destination page displays the correct "Status Codes" heading. | `Navigate to /redirector` → `Click redirect link` → `Wait for h3` → `assertIn("Status Codes", heading.text)` | After the redirect, the page heading contains "Status Codes", confirming the user lands on the correct destination page with the right content. | Cao |
| TC_RL_03 | `test_redirect_invalid_endpoint_tc3` | Kiểm thử âm - Luồng thất bại | Navigate directly to an invalid redirect endpoint URL and verify the Status Codes page is not accidentally displayed. | `Navigate to /redirect/nonexistent_page_404` → `assertNotIn("Status Codes", body_text)` | The "Status Codes" page content is absent, confirming the invalid redirect endpoint correctly does not serve the expected destination page. | Trung bình |
| TC_RL_04 | `test_redirect_link_absent_on_wrong_page_tc4` | Kiểm thử âm - Luồng thất bại | Navigate to the redirect destination page directly and verify the "redirect" trigger link is not present on that page. | `Navigate to /status_codes` → `WebDriverWait(driver, 2).until(presence_of(CSS a[href='redirect']))` → `Catch TimeoutException` | A TimeoutException is raised, confirming the redirect trigger link is exclusive to the `/redirector` page and not present on the destination. | Thấp |

---

## Tính năng: Tải xuống tệp bảo mật
> **Tệp:** test_secure_file_download.py

| Mã Test Case | Tên Hàm | Kỹ thuật | Mô tả Kịch bản | Dữ liệu / Hành động | Kết quả mong đợi | Mức độ ưu tiên |
|---|---|---|---|---|---|---|
| TC_SFD_01 | `test_secure_download_auth_happy_path_tc1` | Phân vùng tương đương - Luồng thành công | Access the secure file download area using valid credentials embedded in the URL and verify that file download links are accessible. | `Navigate to https://admin:admin@.../download_secure` → `Wait for EC.presence_of_element_located(By.CSS_SELECTOR, ".example a")` → `assertTrue(first_link.is_displayed())` | After authenticating, at least one file download link is visible and accessible in the secure area. | Nghiêm trọng |
| TC_SFD_02 | `test_secure_download_unauth_sad_path_tc2` | Kiểm thử bảo mật - Luồng thất bại | Attempt to access the secure file download page without providing any credentials and verify the file links are not accessible. | `Navigate to https://the-internet.herokuapp.com/download_secure` (no credentials)` → `WebDriverWait(driver, 3).until(presence_of(".example a"))` → `Catch TimeoutException` | The file listing is not displayed when no credentials are provided, confirming the download area is protected and inaccessible without authentication. | Nghiêm trọng |

---

## Tính năng: Shadow DOM
> **Tệp:** test_shadow_dom.py

| Mã Test Case | Tên Hàm | Kỹ thuật | Mô tả Kịch bản | Dữ liệu / Hành động | Kết quả mong đợi | Mức độ ưu tiên |
|---|---|---|---|---|---|---|
| TC_SD_01 | `test_shadow_dom_access_via_shadow_root_tc1` | Phân vùng tương đương - Luồng thành công | Use Selenium 4's native Shadow Root API to access the content inside a custom web component and verify the text is readable. | `Navigate to /shadowdom` → `find_element(By.CSS_SELECTOR, "my-paragraph")` → `.shadow_root` → `find_element(By.CSS_SELECTOR, "p")` → `assertTrue(len(text) > 0)` | The inner `<p>` text inside the Shadow DOM is successfully accessed via the Selenium 4 `.shadow_root` property and returns non-empty content. | Cao |
| TC_SD_02 | `test_shadow_dom_access_via_js_tc2` | Phân vùng tương đương - Luồng thành công | Pierce the Shadow DOM boundary using a JavaScript injection and verify the content can be retrieved via script execution. | `execute_script: host.shadowRoot.querySelector('p').textContent` → `assertIsNotNone(text)` → `assertTrue(len(text) > 0)` | The JavaScript injection successfully pierces the Shadow DOM boundary and returns non-empty text content from inside the web component. | Cao |
| TC_SD_03 | `test_shadow_dom_xpath_cannot_pierce_tc3` | Kiểm thử âm - Luồng thất bại | Attempt to locate the Shadow DOM's inner elements using a standard global XPath query and verify it is correctly blocked by the shadow boundary. | `WebDriverWait(driver, 2).until(presence_of(By.XPATH, "//my-paragraph//p[contains(text(),'shadow')]"))` → `Catch TimeoutException or NoSuchElementException` | Standard XPath cannot cross the Shadow DOM boundary, and a timeout or not-found exception is correctly raised, confirming the encapsulation is working. | Trung bình |

---

## Tính năng: Nội dung dịch chuyển
> **Tệp:** test_shifting_content.py

| Mã Test Case | Tên Hàm | Kỹ thuật | Mô tả Kịch bản | Dữ liệu / Hành động | Kết quả mong đợi | Mức độ ưu tiên |
|---|---|---|---|---|---|---|
| TC_SC_01 | `test_tc1_menu_renders_successfully_despite_shifting` | Phân vùng tương đương - Độ bền | Load the shifting content menu page and verify that at least 5 menu items render correctly and that the first item is visible and clickable. | `Navigate to /shifting_content/menu` → `Wait for EC.presence_of_all_elements_located(By.CSS_SELECTOR, "ul li a")` → `assertTrue(len(menu_items) >= 5)` → `assertTrue(first_item.is_displayed() and is_enabled())` | At least 5 shifting menu items are present, and the first item is both visible and interactable, confirming the shifting content page renders reliably. | Trung bình |

---

## Tính năng: Tài nguyên tải chậm
> **Tệp:** test_slow_resources.py

| Mã Test Case | Tên Hàm | Kỹ thuật | Mô tả Kịch bản | Dữ liệu / Hành động | Kết quả mong đợi | Mức độ ưu tiên |
|---|---|---|---|---|---|---|
| TC_SR_01 | `test_slow_resources_full_load_tc1` | Phân vùng tương đương - Luồng thành công | Navigate to the intentionally slow-loading page and verify it fully loads within a generous 30-second window. | `Navigate to /slow` → `WebDriverWait(driver, 30).until(EC.visibility_of_element_located(By.TAG_NAME, "h3"))` → `assertTrue(heading.is_displayed())` | The page heading is visible within 30 seconds, confirming the slow-loading page eventually completes its full load cycle. | Cao |
| TC_SR_02 | `test_slow_resources_perf_entry_exists_tc2` | Phân vùng tương đương - Độ bền | After loading the slow page, query the browser's Performance API to verify a navigation timing entry exists with a non-zero duration. | `WebDriverWait(driver, 30)` → `execute_script("return window.performance.getEntriesByType('navigation')")` → `assertGreater(len(entries), 0)` → `assertGreater(duration, 0)` | At least one navigation performance entry exists with a duration greater than 0ms, confirming a real network round-trip occurred and is being measured. | Trung bình |
| TC_SR_03 | `test_slow_resources_page_structure_tc3` | Phân vùng tương đương - Luồng thành công | After the slow page loads, verify the current URL contains "/slow" and the page heading is not empty. | `WebDriverWait(driver, 30)` → `assertIn("/slow", driver.current_url)` → `assertTrue(len(heading_text) > 0)` | The URL contains "/slow" and the page heading is non-empty, confirming the correct page loaded with valid content. | Trung bình |

---

## Tính năng: Bảng dữ liệu có thể sắp xếp
> **Tệp:** test_sortable_data_tables.py

| Mã Test Case | Tên Hàm | Kỹ thuật | Mô tả Kịch bản | Dữ liệu / Hành động | Kết quả mong đợi | Mức độ ưu tiên |
|---|---|---|---|---|---|---|
| TC_SDT_01 | `test_sortable_tables_sort_lastname_asc_tc1` | Phân vùng tương đương - Luồng thành công | Click the "Last Name" column header once and verify the column data is sorted in ascending alphabetical order. | `Navigate to /tables` → `Click XPath //table[@id='table1']//th[span[text()='Last Name']]` → `_get_column_values("table1", 1)` → `assertEqual(actual, sorted(actual))` | The "Last Name" column is sorted in ascending (A-Z) alphabetical order after a single click on the column header. | Cao |
| TC_SDT_02 | `test_sortable_tables_sort_lastname_desc_tc2` | Phân vùng tương đương - Luồng thành công | Click the "Last Name" column header twice and verify the data reverses to a descending (Z-A) sort order. | `Click header twice` → `_get_column_values("table1", 1)` → `assertEqual(actual, sorted(actual, reverse=True))` | The "Last Name" column is sorted in descending (Z-A) order after the second click on the header, confirming the toggle sort works. | Cao |
| TC_SDT_03 | `test_sortable_tables_unsortable_column_tc3` | Phân tích giá trị biên - Luồng thành công | Click the "Email" column header in Table 2 and verify it is also sortable, returning data in alphabetical order. | `Click XPath //table[@id='table2']//th[span[text()='Email']]` → `_get_column_values("table2", 3)` → `assertEqual(values_after, sorted(values_after))` | The Email column in Table 2 is successfully sorted alphabetically after clicking the header, confirming all columns in both tables are sortable. | Trung bình |
| TC_SDT_04 | `test_sortable_tables_out_of_bounds_column_tc4` | Kiểm thử âm - Luồng thất bại | Attempt to extract data from a non-existent column index (99) and verify the system returns an empty result gracefully. | `_get_column_values("table1", col_index=99)` → `assertEqual(values, [])` | An empty list is returned for the out-of-bounds column index, confirming the helper method handles invalid column requests gracefully without crashing. | Thấp |

---

## Tính năng: Mã trạng thái HTTP
> **Tệp:** test_status_codes.py

| Mã Test Case | Tên Hàm | Kỹ thuật | Mô tả Kịch bản | Dữ liệu / Hành động | Kết quả mong đợi | Mức độ ưu tiên |
|---|---|---|---|---|---|---|
| TC_STC_01 | `test_tc1_status_code_200_ok` | Phân vùng tương đương - Luồng thành công | Click the "200" link and verify the destination page confirms a successful HTTP 200 OK response. | `Navigate to /status_codes` → `Click link "200"` → `Wait for .example p` → `assertIn("This page returned a 200 status code.", status_text)` | The page confirms receipt of a 200 OK status code, indicating a fully successful response. | Cao |
| TC_STC_02 | `test_tc2_status_code_301_moved` | Phân vùng tương đương - Luồng thành công | Click the "301" link and verify the destination page confirms a 301 Moved Permanently redirect response. | `Navigate to /status_codes` → `Click link "301"` → `assertIn("This page returned a 301 status code.", status_text)` | The page confirms receipt of a 301 status code, indicating the resource has been permanently moved. | Trung bình |
| TC_STC_03 | `test_tc3_status_code_404_not_found` | Kiểm thử âm - Luồng thất bại | Click the "404" link and verify the destination page correctly identifies the Not Found error response. | `Navigate to /status_codes` → `Click link "404"` → `assertIn("This page returned a 404 status code.", status_text)` | The page confirms receipt of a 404 status code, indicating the requested resource was not found on the server. | Cao |
| TC_STC_04 | `test_tc4_status_code_500_server_error` | Kiểm thử âm - Luồng thất bại | Click the "500" link and verify the destination page correctly identifies the Internal Server Error response. | `Navigate to /status_codes` → `Click link "500"` → `assertIn("This page returned a 500 status code.", status_text)` | The page confirms receipt of a 500 status code, indicating a server-side error, with the application handling it gracefully. | Cao |

---

## Tính năng: Phát hiện lỗi chính tả (A/B)
> **Tệp:** test_typos.py

| Mã Test Case | Tên Hàm | Kỹ thuật | Mô tả Kịch bản | Dữ liệu / Hành động | Kết quả mong đợi | Mức độ ưu tiên |
|---|---|---|---|---|---|---|
| TC_TY_01 | `test_typos_refresh_until_correct_tc1` | Phân vùng tương đương - Luồng thành công | Refresh the page up to 10 times until the grammatically correct version of the sentence ("won't") appears, then stop. | `Loop up to 10×: Navigate to /typos` → `_get_second_paragraph()` → `If CORRECT_TEXT in text: break` → `assertTrue(found_correct)` | The correct version of the sentence (containing "won't") is found within 10 page loads, confirming the page does serve the correct content variant. | Trung bình |
| TC_TY_02 | `test_typos_detect_known_typo_tc2` | Kiểm thử âm - Phát hiện lỗi | Load the page and scan for the known A/B typo variant ("won,t") within 10 attempts, logging it as a content defect if found. | `Loop up to 10×: Navigate to /typos` → `_get_second_paragraph()` → `If TYPO_TEXT in text: found_typo = True; break` → `Log result` | Either the known typo ("won,t") is detected and logged as an A/B content defect, or the correct variant is observed. Either outcome is a pass — the goal is detection and documentation. | Trung bình |
| TC_TY_03 | `test_typos_page_structure_robustness_tc3` | Phân vùng tương đương - Độ bền | Verify the page always renders exactly 2 paragraphs regardless of which A/B content variant is served. | `Navigate to /typos` → `find_elements(By.CSS_SELECTOR, "div.example p")` → `assertEqual(len(paragraphs), 2)` → `assertIn(second_text, known_variants)` | The page always has exactly 2 paragraphs, and the second paragraph is always one of the two known A/B variants, confirming structural consistency. | Trung bình |

---

## Tính năng: Trình soạn thảo WYSIWYG (TinyMCE)
> **Tệp:** test_wysiwyg_editor.py

| Mã Test Case | Tên Hàm | Kỹ thuật | Mô tả Kịch bản | Dữ liệu / Hành động | Kết quả mong đợi | Mức độ ưu tiên |
|---|---|---|---|---|---|---|
| TC_WYS_01 | `test_wysiwyg_js_injection_happy_path_tc1` | Phân vùng tương đương - Luồng thành công | Switch into the TinyMCE iFrame, inject custom text into the editor body using JavaScript, and verify the content is correctly written. | `Navigate to /tinymce` → `Wait for EC.frame_to_be_available_and_switch_to_it(By.ID, "mce_0_ifr")` → `execute_script: editor_body.innerHTML = "<p>INJECT_TEXT</p>"` → `assertIn(INJECT_TEXT, innerHTML)` | The injected text is confirmed present in the TinyMCE editor's HTML body, proving that JavaScript-level content injection bypasses the read-only constraint. | Cao |
| TC_WYS_02 | `test_wysiwyg_readonly_alert_sad_path_tc2` | Kiểm thử âm - Độ bền | Load the TinyMCE editor page and check whether a read-only API-limit warning overlay appears, handling either outcome as a valid test result. | `Navigate to /tinymce` → `WebDriverWait(driver, 5).until(presence_of(".tox-notification--warning"))` → `assertTrue(warning_overlay.is_displayed())` OR `Catch TimeoutException` | If the read-only overlay is present, it is correctly identified and verified. If absent (TinyMCE loaded normally), the test also passes — both are valid states for this demo app. | Trung bình |
| TC_WYS_03 | `test_wysiwyg_toolbar_visibility_happy_path_tc3` | Phân vùng tương đương - Luồng thành công | Load the WYSIWYG editor page and verify that the Bold and Italic toolbar buttons are visible in the main document context. | `Navigate to /tinymce` → `Wait for .tox-toolbar__primary` → `find_element(XPath //button[@aria-label='Bold'])` → `assertTrue(bold_btn.is_displayed())` → same for `Italic` | Both the Bold and Italic toolbar buttons are visible and rendered in the TinyMCE toolbar, confirming the editor UI loaded correctly. | Cao |
| TC_WYS_04 | `test_wysiwyg_context_isolation_sad_path_tc4` | Kiểm thử âm - Luồng thất bại | Switch into the TinyMCE iFrame and then attempt to find the main-document toolbar buttons, verifying they are invisible from inside the frame context. | `frame_to_be_available_and_switch_to_it(By.ID, "mce_0_ifr")` → `try find_element(XPath //button[@aria-label='Bold'])` → `Catch NoSuchElementException` | A NoSuchElementException is raised because toolbar buttons live in the main document, not inside the iFrame, confirming correct context isolation. | Trung bình |

---

## Tổng kết

| # | Feature | File | Tổng TC | Nghiêm trọng | Cao | Trung bình | Thấp |
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
| | **TỔNG CỘNG** | **44 tệp** | **128** | **12** | **57** | **52** | **9** |

---
*Được tạo bởi Kiến trúc sư QA tự động hóa cấp cao · Dịch ngược từ mã nguồn · 2026-05-07*
