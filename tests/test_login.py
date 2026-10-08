import sys
import os
import time
import unittest
import allure

# Đảm bảo đường dẫn gốc của project luôn nằm trong sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import config
from base.base_test import BaseTest

@allure.epic("Hệ Thống Văn Phòng Điện Tử UTC")
@allure.feature("Phân hệ Đăng nhập (Authentication)")
class TestLogin(BaseTest):
    """
    Bộ 20 ca kiểm thử tự động cho chức năng Đăng nhập Văn phòng điện tử UTC
    Kế thừa từ BaseTest (quản lý vòng đời WebDriver tự động).
    Khớp chính xác với file kịch bản TestCases_VanPhongDienTu_UTC.xlsx
    Tích hợp Allure Report báo cáo trực quan, chi tiết từng bước (steps, screenshots, severities).
    """

    # =========================================================================
    # NHÓM 1: KIỂM THỬ CHỨC NĂNG CƠ BẢN (TC01 - TC07)
    # =========================================================================

    @allure.story("Kiểm tra tính hợp lệ dữ liệu (Validation)")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("TC01 - Để trống Tên đăng nhập (chỉ nhập Mật khẩu)")
    @allure.description("Kiểm tra hệ thống hiển thị thông báo lỗi 'Bạn chưa nhập tên đăng nhập' khi để trống Tên đăng nhập và chỉ nhập Mật khẩu.")
    def test_tc01_empty_username(self):
        """TC01: Để trống Tên đăng nhập (chỉ nhập Mật khẩu)"""
        with allure.step("1. Nhập mật khẩu hợp lệ: '1256'"):
            self.login_page.enter_password("1256")
            
        with allure.step("2. Nhấn nút Đăng nhập"):
            self.login_page.click_login()
        
        with allure.step("3. Kiểm tra thông báo lỗi và chụp ảnh minh chứng"):
            error_msg = self.login_page.get_error_message()
            self.login_page.capture_screenshot("TC01_empty_username.png")
            self.assertIn("Bạn chưa nhập tên đăng nhập", error_msg, 
                          f"Thông báo lỗi không đúng kỳ vọng. Nhận được: '{error_msg}'")

    @allure.story("Kiểm tra tính hợp lệ dữ liệu (Validation)")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("TC02 - Để trống Mật khẩu (chỉ nhập Tên đăng nhập)")
    @allure.description("Kiểm tra hệ thống hiển thị thông báo lỗi 'Bạn chưa nhập mật khẩu' khi chỉ nhập Tên đăng nhập và để trống Mật khẩu.")
    def test_tc02_empty_password(self):
        """TC02: Để trống Mật khẩu (chỉ nhập Tên đăng nhập)"""
        with allure.step("1. Nhập tên đăng nhập: 'huongnt'"):
            self.login_page.enter_username("huongnt")
            
        with allure.step("2. Nhấn nút Đăng nhập"):
            self.login_page.click_login()
        
        with allure.step("3. Kiểm tra thông báo lỗi và chụp ảnh minh chứng"):
            error_msg = self.login_page.get_error_message()
            self.login_page.capture_screenshot("TC02_empty_password.png")
            self.assertIn("Bạn chưa nhập mật khẩu", error_msg,
                          f"Thông báo lỗi không đúng kỳ vọng. Nhận được: '{error_msg}'")

    @allure.story("Xác thực tài khoản (Authentication)")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("TC03 - Nhập đúng Tên đăng nhập, sai Mật khẩu")
    @allure.description("Kiểm tra hệ thống từ chối đăng nhập khi nhập đúng định dạng Tên đăng nhập nhưng Mật khẩu sai.")
    def test_tc03_correct_user_wrong_pass(self):
        """TC03: Nhập đúng Tên đăng nhập, sai Mật khẩu"""
        with allure.step("1. Nhập tên đăng nhập: 'huongnt'"):
            self.login_page.enter_username("huongnt")
            
        with allure.step("2. Nhập mật khẩu không chính xác: 'utc@235'"):
            self.login_page.enter_password("utc@235")
            
        with allure.step("3. Nhấn nút Đăng nhập"):
            self.login_page.click_login()
        
        with allure.step("4. Kiểm tra thông báo lỗi và chụp ảnh minh chứng"):
            error_msg = self.login_page.get_error_message()
            self.login_page.capture_screenshot("TC03_wrong_pass.png")
            self.assertTrue("Tài khoản" in error_msg or "mật khẩu" in error_msg,
                            f"Thông báo lỗi không đúng kỳ vọng. Nhận được: '{error_msg}'")

    @allure.story("Xác thực tài khoản (Authentication)")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("TC04 - Nhập sai Tên đăng nhập, đúng định dạng Mật khẩu")
    @allure.description("Kiểm tra hệ thống từ chối khi nhập tài khoản không tồn tại trên hệ thống.")
    def test_tc04_wrong_user_valid_pass(self):
        """TC04: Nhập sai Tên đăng nhập, đúng định dạng Mật khẩu"""
        with allure.step("1. Nhập tên đăng nhập không tồn tại: 'huongthunguyen'"):
            self.login_page.enter_username("huongthunguyen")
            
        with allure.step("2. Nhập mật khẩu đúng định dạng: '123456@utc'"):
            self.login_page.enter_password("123456@utc")
            
        with allure.step("3. Nhấn nút Đăng nhập"):
            self.login_page.click_login()
        
        with allure.step("4. Kiểm tra thông báo lỗi và chụp ảnh minh chứng"):
            error_msg = self.login_page.get_error_message()
            self.login_page.capture_screenshot("TC04_wrong_user.png")
            self.assertTrue("Tài khoản" in error_msg or "mật khẩu" in error_msg,
                            f"Thông báo lỗi không đúng kỳ vọng. Nhận được: '{error_msg}'")

    @allure.story("Đăng nhập thành công & Duy trì phiên")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("TC05 - Đăng nhập thành công và chọn 'Giữ tôi luôn đăng nhập'")
    @allure.description("Kiểm tra tính năng đăng nhập kết hợp lưu phiên làm việc với checkbox 'Giữ tôi luôn đăng nhập'.")
    def test_tc05_login_with_remember_me(self):
        """TC05: Đăng nhập thành công và chọn 'Giữ tôi luôn đăng nhập'"""
        with allure.step(f"1. Nhập tài khoản: '{config.VALID_USERNAME}' và mật khẩu"):
            self.login_page.enter_username(config.VALID_USERNAME)
            self.login_page.enter_password(config.VALID_PASSWORD)
            
        with allure.step("2. Tích chọn checkbox 'Giữ tôi luôn đăng nhập'"):
            self.login_page.set_remember_me(True)
            self.assertTrue(self.login_page.is_remember_me_checked(),
                            "Checkbox 'Giữ tôi luôn đăng nhập' chưa được tích chọn")
            
        with allure.step("3. Nhấn nút Đăng nhập"):
            self.login_page.click_login()
            time.sleep(1.5)
            self.login_page.capture_screenshot("TC05_remember_me_checked.png")
        
        with allure.step("4. Kiểm tra phản hồi thực tế từ hệ thống"):
            error_msg = self.login_page.get_error_message(timeout=3)
            self.assertEqual(error_msg, "", 
                             f"Đăng nhập thất bại: Hệ thống báo '{error_msg}'. "
                             f"(Tài khoản '{config.VALID_USERNAME}' không tồn tại hoặc sai mật khẩu trên máy chủ UTC)")

    @allure.story("Đăng nhập thành công & Duy trì phiên")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("TC06 - Đăng nhập thành công và không chọn 'Giữ tôi luôn đăng nhập'")
    @allure.description("Kiểm tra tính năng đăng nhập tiêu chuẩn khi không tích chọn 'Giữ tôi luôn đăng nhập'.")
    def test_tc06_login_without_remember_me(self):
        """TC06: Đăng nhập thành công và không chọn 'Giữ tôi luôn đăng nhập'"""
        with allure.step(f"1. Nhập tài khoản: '{config.VALID_USERNAME}' và mật khẩu"):
            self.login_page.enter_username(config.VALID_USERNAME)
            self.login_page.enter_password(config.VALID_PASSWORD)
            
        with allure.step("2. Đảm bảo bỏ tích checkbox 'Giữ tôi luôn đăng nhập'"):
            self.login_page.set_remember_me(False)
            self.assertFalse(self.login_page.is_remember_me_checked(),
                             "Checkbox 'Giữ tôi luôn đăng nhập' không nên được tích chọn")
            
        with allure.step("3. Nhấn nút Đăng nhập"):
            self.login_page.click_login()
            time.sleep(1.5)
            self.login_page.capture_screenshot("TC06_remember_me_unchecked.png")
        
        with allure.step("4. Kiểm tra phản hồi thực tế từ hệ thống"):
            error_msg = self.login_page.get_error_message(timeout=3)
            self.assertEqual(error_msg, "", 
                             f"Đăng nhập thất bại: Hệ thống báo '{error_msg}'. "
                             f"(Tài khoản '{config.VALID_USERNAME}' không tồn tại hoặc sai mật khẩu trên máy chủ UTC)")

    @allure.story("Kiểm tra tính hợp lệ dữ liệu (Validation)")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("TC07 - Để trống cả Tên đăng nhập và Mật khẩu")
    @allure.description("Kiểm tra hệ thống hiển thị thông báo lỗi khi để trống cả 2 trường Tên đăng nhập và Mật khẩu.")
    def test_tc07_empty_all(self):
        """TC07: Để trống cả Tên đăng nhập và Mật khẩu"""
        with allure.step("1. Để trống Tên đăng nhập và Mật khẩu"):
            self.login_page.enter_username("")
            self.login_page.enter_password("")
            
        with allure.step("2. Nhấn nút Đăng nhập"):
            self.login_page.click_login()
        
        with allure.step("3. Kiểm tra thông báo lỗi hiển thị và chụp ảnh minh chứng"):
            error_msg = self.login_page.get_error_message()
            self.login_page.capture_screenshot("TC07_empty_all.png")
            self.assertIn("Bạn chưa nhập tên đăng nhập", error_msg,
                          f"Thông báo lỗi không đúng kỳ vọng. Nhận được: '{error_msg}'")

    # =========================================================================
    # NHÓM 2: GIAO DIỆN & LIÊN KẾT LIÊN QUAN (TC08 - TC10)
    # =========================================================================

    @allure.story("Giao diện UI & Tính bảo mật thông tin")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("TC08 - Kiểm tra tính năng ẩn mật khẩu (Masked characters)")
    @allure.description("Kiểm tra trường Mật khẩu được thiết lập type='password' để che giấu ký tự bảo mật.")
    def test_tc08_password_masked(self):
        """TC08: Kiểm tra tính năng ẩn mật khẩu (Masked characters)"""
        with allure.step("1. Kiểm tra thuộc tính type của trường Mật khẩu"):
            is_masked = self.login_page.is_password_masked()
            self.login_page.capture_screenshot("TC08_password_masked.png")
            self.assertTrue(is_masked, "Ô mật khẩu không có thuộc tính type='password'")

    @allure.story("Liên kết SSO & Đăng nhập một lần")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("TC09 - Kiểm tra chức năng liên kết 'Đăng nhập bằng e-mail UTC'")
    @allure.description("Kiểm tra liên kết SSO liên kết chính xác tới hệ thống xác thực Google OAuth UTC.")
    def test_tc09_google_sso_link(self):
        """TC09: Kiểm tra chức năng liên kết 'Đăng nhập bằng e-mail UTC'"""
        with allure.step("1. Lấy thuộc tính href của liên kết Đăng nhập bằng e-mail UTC"):
            google_href = self.login_page.get_google_login_href()
            self.login_page.capture_screenshot("TC09_google_sso.png")
            
        with allure.step("2. Kiểm tra đích đến của liên kết SSO"):
            self.assertTrue("accounts.google.com" in google_href or "oauth2" in google_href,
                            f"Đường dẫn đăng nhập qua Google UTC không hợp lệ: {google_href}")

    @allure.story("Điều hướng & Khôi phục mật khẩu")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("TC10 - Kiểm tra liên kết 'Bạn quên mật khẩu đăng nhập ?'")
    @allure.description("Kiểm tra liên kết quên mật khẩu chuyển hướng đến đúng trang Lấy lại mật khẩu (/Login/GetPass).")
    def test_tc10_forgot_password_link(self):
        """TC10: Kiểm tra liên kết 'Bạn quên mật khẩu đăng nhập ?'"""
        with allure.step("1. Nhấn vào liên kết 'Bạn quên mật khẩu đăng nhập ?'"):
            self.login_page.click_forgot_password()
            time.sleep(1.5)
            
        with allure.step("2. Xác minh URL và tiêu đề trang chuyển hướng"):
            current_url = self.login_page.get_current_url()
            page_title = self.login_page.get_title()
            self.login_page.capture_screenshot("TC10_forgot_password.png")
            self.assertTrue("GetPass" in current_url,
                            f"URL không chuyển hướng tới trang GetPass. Hiện tại: {current_url}")
            self.assertIn("Lấy lại mật khẩu", page_title,
                          f"Tiêu đề trang không đúng. Hiện tại: '{page_title}'")

    # =========================================================================
    # NHÓM 3: KIỂM THỬ NÂNG CAO, BẢO MẬT & TRẢI NGHIỆM (TC11 - TC20)
    # =========================================================================

    @allure.story("Trải nghiệm người dùng (UX) & Phím tắt")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("TC11 - Đăng nhập bằng cách nhấn phím Enter từ bàn phím")
    @allure.description("Kiểm tra form đăng nhập tự động gửi đi khi nhấn phím Enter tại trường Mật khẩu.")
    def test_tc11_login_with_enter_key(self):
        """TC11: Đăng nhập bằng cách nhấn phím Enter từ bàn phím"""
        with allure.step("1. Nhập mật khẩu '1256' và nhấn phím ENTER"):
            self.login_page.press_enter_on_password("1256")
            time.sleep(1)
            
        with allure.step("2. Xác minh form đã gửi và hiển thị kiểm tra validate"):
            error_msg = self.login_page.get_error_message()
            self.login_page.capture_screenshot("TC11_enter_key.png")
            self.assertIn("Bạn chưa nhập tên đăng nhập", error_msg,
                          f"Nhấn Enter không kích hoạt gửi form kiểm tra: '{error_msg}'")

    @allure.story("Kiểm tra tính hợp lệ dữ liệu (Validation)")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("TC12 - Tên đăng nhập chỉ chứa toàn khoảng trắng (Space-only)")
    @allure.description("Kiểm tra hệ thống từ chối giá trị Tên đăng nhập chỉ toàn ký tự trắng.")
    def test_tc12_space_only_username(self):
        """TC12: Tên đăng nhập chỉ chứa toàn khoảng trắng (Space-only)"""
        with allure.step("1. Nhập khoảng trắng vào Tên đăng nhập và mật khẩu hợp lệ"):
            self.login_page.enter_username("   ")
            self.login_page.enter_password("123456")
            
        with allure.step("2. Nhấn nút Đăng nhập"):
            self.login_page.click_login()
            time.sleep(1)
            
        with allure.step("3. Kiểm tra hệ thống từ chối khoảng trắng"):
            error_msg = self.login_page.get_error_message()
            self.login_page.capture_screenshot("TC12_space_only_username.png")
            self.assertTrue("Tài khoản" in error_msg or "mật khẩu" in error_msg or "chưa nhập" in error_msg,
                            f"Hệ thống không từ chối khoảng trắng hợp lệ. Nhận được: '{error_msg}'")

    @allure.story("Kiểm tra tính hợp lệ dữ liệu (Validation)")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("TC13 - Mật khẩu chỉ chứa toàn khoảng trắng (Space-only)")
    @allure.description("Kiểm tra hệ thống từ chối giá trị Mật khẩu chỉ toàn ký tự trắng.")
    def test_tc13_space_only_password(self):
        """TC13: Mật khẩu chỉ chứa toàn khoảng trắng (Space-only)"""
        with allure.step("1. Nhập Tên đăng nhập hợp lệ và Mật khẩu toàn khoảng trắng"):
            self.login_page.enter_username("huongnt")
            self.login_page.enter_password("   ")
            
        with allure.step("2. Nhấn nút Đăng nhập"):
            self.login_page.click_login()
            time.sleep(1)
            
        with allure.step("3. Kiểm tra hệ thống từ chối khoảng trắng"):
            error_msg = self.login_page.get_error_message()
            self.login_page.capture_screenshot("TC13_space_only_password.png")
            self.assertTrue("Tài khoản" in error_msg or "mật khẩu" in error_msg or "chưa nhập" in error_msg,
                            f"Hệ thống không từ chối khoảng trắng hợp lệ. Nhận được: '{error_msg}'")

    @allure.story("Kiểm thử bảo mật (Security Testing)")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("TC14 - Kiểm tra khả năng chống tấn công SQL Injection cơ bản")
    @allure.description("Kiểm tra hệ thống xử lý an toàn với payload SQL Injection, không crash hoặc bypass.")
    def test_tc14_sql_injection(self):
        """TC14: Kiểm tra khả năng chống tấn công SQL Injection cơ bản"""
        with allure.step("1. Nhập payload SQL Injection: \"' OR '1'='1\""):
            self.login_page.enter_username("' OR '1'='1")
            self.login_page.enter_password("123456")
            
        with allure.step("2. Nhấn nút Đăng nhập"):
            self.login_page.click_login()
            time.sleep(1)
            
        with allure.step("3. Kiểm tra phản hồi an toàn"):
            error_msg = self.login_page.get_error_message()
            self.login_page.capture_screenshot("TC14_sql_injection.png")
            self.assertTrue("Tài khoản" in error_msg or "mật khẩu" in error_msg,
                            f"Hệ thống xử lý SQL Injection không an toàn: '{error_msg}'")

    @allure.story("Kiểm thử bảo mật (Security Testing)")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("TC15 - Kiểm tra khả năng chống tấn công XSS Script Injection")
    @allure.description("Kiểm tra hệ thống không thực thi đoạn script JavaScript độc hại trong trường nhập liệu.")
    def test_tc15_xss_injection(self):
        """TC15: Kiểm tra khả năng chống tấn công XSS Script Injection"""
        with allure.step("1. Nhập payload XSS: \"<script>alert(1)</script>\""):
            self.login_page.enter_username("<script>alert(1)</script>")
            self.login_page.enter_password("123456")
            
        with allure.step("2. Nhấn nút Đăng nhập"):
            self.login_page.click_login()
            time.sleep(1)
            
        with allure.step("3. Kiểm tra script không thực thi và hệ thống xử lý an toàn"):
            error_msg = self.login_page.get_error_message()
            self.login_page.capture_screenshot("TC15_xss_injection.png")
            self.assertTrue("Tài khoản" in error_msg or "mật khẩu" in error_msg,
                            f"Hệ thống xử lý XSS không an toàn: '{error_msg}'")

    @allure.story("Kiểm thử giá trị biên (Boundary Testing)")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("TC16 - Nhập Tên đăng nhập có độ dài cực đại (300 ký tự)")
    @allure.description("Kiểm tra hệ thống xử lý ổn định chuỗi ký tự độ dài biên 300 ký tự mà không bị tràn bộ nhớ hay vỡ layout.")
    def test_tc16_boundary_long_string(self):
        """TC16: Nhập Tên đăng nhập có độ dài cực đại (300 ký tự)"""
        with allure.step("1. Nhập chuỗi 300 ký tự vào Tên đăng nhập"):
            self.login_page.enter_username("a" * 300)
            self.login_page.enter_password("123456")
            
        with allure.step("2. Nhấn nút Đăng nhập"):
            self.login_page.click_login()
            time.sleep(1)
            
        with allure.step("3. Kiểm tra hệ thống từ chối an toàn"):
            error_msg = self.login_page.get_error_message()
            self.login_page.capture_screenshot("TC16_long_username.png")
            self.assertTrue("Tài khoản" in error_msg or "mật khẩu" in error_msg,
                            f"Hệ thống xử lý chuỗi dài không đúng: '{error_msg}'")

    @allure.story("Kiểm tra tính hợp lệ dữ liệu (Validation)")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("TC17 - Tên đăng nhập chứa tập ký tự đặc biệt (!@#$%^&*())")
    @allure.description("Kiểm tra hệ thống tiếp nhận và xử lý chuẩn xác khi tài khoản chứa chuỗi ký tự đặc biệt.")
    def test_tc17_special_characters(self):
        """TC17: Tên đăng nhập chứa tập ký tự đặc biệt (!@#$%^&*())"""
        with allure.step("1. Nhập ký tự đặc biệt vào Tên đăng nhập"):
            self.login_page.enter_username("admin!@#$%^&*()")
            self.login_page.enter_password("123456")
            
        with allure.step("2. Nhấn nút Đăng nhập"):
            self.login_page.click_login()
            time.sleep(1)
            
        with allure.step("3. Kiểm tra thông báo lỗi"):
            error_msg = self.login_page.get_error_message()
            self.login_page.capture_screenshot("TC17_special_chars.png")
            self.assertTrue("Tài khoản" in error_msg or "mật khẩu" in error_msg,
                            f"Hệ thống xử lý ký tự đặc biệt không đúng: '{error_msg}'")

    @allure.story("Giao diện UI & Trải nghiệm người dùng")
    @allure.severity(allure.severity_level.MINOR)
    @allure.title("TC18 - Kiểm tra văn bản gợi ý (Placeholder) trên các trường nhập liệu")
    @allure.description("Kiểm tra thuộc tính placeholder: Username là 'Tên đăng nhập' và Password là 'Mật khẩu'.")
    def test_tc18_placeholders(self):
        """TC18: Kiểm tra văn bản gợi ý (Placeholder) trên các trường nhập liệu"""
        with allure.step("1. Lấy giá trị placeholder từ 2 trường nhập liệu"):
            user_ph = self.login_page.get_username_placeholder()
            pwd_ph = self.login_page.get_password_placeholder()
            self.login_page.capture_screenshot("TC18_placeholders.png")
            
        with allure.step("2. So sánh với quy chuẩn giao diện"):
            self.assertEqual(user_ph, "Tên đăng nhập", f"Placeholder Username không đúng: '{user_ph}'")
            self.assertEqual(pwd_ph, "Mật khẩu", f"Placeholder Password không đúng: '{pwd_ph}'")

    @allure.story("Trải nghiệm người dùng (UX) & Phím tắt")
    @allure.severity(allure.severity_level.MINOR)
    @allure.title("TC19 - Kiểm tra điều hướng chuyển con trỏ nhập liệu bằng phím Tab")
    @allure.description("Kiểm tra khi nhấn phím Tab từ trường Tên đăng nhập, con trỏ tự động chuyển sang trường Mật khẩu.")
    def test_tc19_tab_key_navigation(self):
        """TC19: Kiểm tra điều hướng chuyển con trỏ nhập liệu bằng phím Tab"""
        with allure.step("1. Nhấn phím Tab từ ô Tên đăng nhập"):
            focused_elem_name = self.login_page.navigate_with_tab_key()
            self.login_page.capture_screenshot("TC19_tab_navigation.png")
            
        with allure.step("2. Kiểm tra focus đã chuyển sang ô mật khẩu (userpwd)"):
            self.assertEqual(focused_elem_name, "userpwd",
                             f"Phím Tab không chuyển focus tới ô mật khẩu (userpwd). Nhận được: '{focused_elem_name}'")

    @allure.story("Giao diện UI & Liên kết hỗ trợ")
    @allure.severity(allure.severity_level.MINOR)
    @allure.title("TC20 - Kiểm tra tính đúng đắn của các liên kết hỗ trợ ở chân trang (Footer)")
    @allure.description("Kiểm tra link 'Trung tâm trợ giúp' trỏ về hotrokythuat.utc.edu.vn và liên kết 'Ý kiến phản hồi' mở mailto.")
    def test_tc20_footer_links(self):
        """TC20: Kiểm tra tính đúng đắn của các liên kết hỗ trợ ở chân trang (Footer)"""
        with allure.step("1. Lấy thuộc tính href của 2 liên kết chân trang"):
            help_href = self.login_page.get_help_center_href()
            feedback_href = self.login_page.get_feedback_href()
            self.login_page.capture_screenshot("TC20_footer_links.png")
            
        with allure.step("2. Xác minh tính chính xác của các đường dẫn hỗ trợ"):
            self.assertTrue("hotrokythuat.utc.edu.vn" in help_href,
                            f"Link Trung tâm trợ giúp không hợp lệ: '{help_href}'")
            self.assertTrue("mailto:hotrokythuat@utc.edu.vn" in feedback_href,
                            f"Link Ý kiến phản hồi không hợp lệ: '{feedback_href}'")

if __name__ == '__main__':
    unittest.main()
