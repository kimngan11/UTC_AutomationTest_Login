import sys
import os
import time
import unittest

# Đảm bảo đường dẫn gốc của project luôn nằm trong sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import config
from base.base_test import BaseTest

class TestLogin(BaseTest):
    """
    Bộ 20 ca kiểm thử tự động cho chức năng Đăng nhập Văn phòng điện tử UTC
    Kế thừa từ BaseTest (quản lý vòng đời WebDriver tự động).
    Khớp chính xác với file kịch bản TestCases_VanPhongDienTu_UTC.xlsx
    """

    # =========================================================================
    # NHÓM 1: KIỂM THỬ CHỨC NĂNG CƠ BẢN (TC01 - TC07)
    # =========================================================================

    def test_tc01_empty_username(self):
        """TC01: Để trống Tên đăng nhập (chỉ nhập Mật khẩu)"""
        self.login_page.enter_password("1256")
        self.login_page.click_login()
        
        error_msg = self.login_page.get_error_message()
        self.login_page.capture_screenshot("TC01_empty_username.png")
        self.assertIn("Bạn chưa nhập tên đăng nhập", error_msg, 
                      f"Thông báo lỗi không đúng kỳ vọng. Nhận được: '{error_msg}'")

    def test_tc02_empty_password(self):
        """TC02: Để trống Mật khẩu (chỉ nhập Tên đăng nhập)"""
        self.login_page.enter_username("huongnt")
        self.login_page.click_login()
        
        error_msg = self.login_page.get_error_message()
        self.login_page.capture_screenshot("TC02_empty_password.png")
        self.assertIn("Bạn chưa nhập mật khẩu", error_msg,
                      f"Thông báo lỗi không đúng kỳ vọng. Nhận được: '{error_msg}'")

    def test_tc03_correct_user_wrong_pass(self):
        """TC03: Nhập đúng Tên đăng nhập, sai Mật khẩu"""
        self.login_page.enter_username("huongnt")
        self.login_page.enter_password("utc@235")
        self.login_page.click_login()
        
        error_msg = self.login_page.get_error_message()
        self.login_page.capture_screenshot("TC03_wrong_pass.png")
        self.assertTrue("Tài khoản" in error_msg or "mật khẩu" in error_msg,
                        f"Thông báo lỗi không đúng kỳ vọng. Nhận được: '{error_msg}'")

    def test_tc04_wrong_user_valid_pass(self):
        """TC04: Nhập sai Tên đăng nhập, đúng định dạng Mật khẩu"""
        self.login_page.enter_username("huongthunguyen")
        self.login_page.enter_password("123456@utc")
        self.login_page.click_login()
        
        error_msg = self.login_page.get_error_message()
        self.login_page.capture_screenshot("TC04_wrong_user.png")
        self.assertTrue("Tài khoản" in error_msg or "mật khẩu" in error_msg,
                        f"Thông báo lỗi không đúng kỳ vọng. Nhận được: '{error_msg}'")

    def test_tc05_login_with_remember_me(self):
        """TC05: Đăng nhập thành công và chọn 'Giữ tôi luôn đăng nhập'"""
        self.login_page.enter_username(config.VALID_USERNAME)
        self.login_page.enter_password(config.VALID_PASSWORD)
        self.login_page.set_remember_me(True)
        
        self.assertTrue(self.login_page.is_remember_me_checked(),
                        "Checkbox 'Giữ tôi luôn đăng nhập' chưa được tích chọn")
        self.login_page.click_login()
        time.sleep(1.5)
        self.login_page.capture_screenshot("TC05_remember_me_checked.png")
        
        # Kiểm tra phản hồi thực tế (nếu tài khoản demo huongnt không tồn tại trên hệ thống thật thì báo lỗi)
        error_msg = self.login_page.get_error_message(timeout=3)
        self.assertEqual(error_msg, "", 
                         f"Đăng nhập thất bại: Hệ thống báo '{error_msg}'. "
                         f"(Tài khoản '{config.VALID_USERNAME}' không tồn tại hoặc sai mật khẩu trên máy chủ UTC)")

    def test_tc06_login_without_remember_me(self):
        """TC06: Đăng nhập thành công và không chọn 'Giữ tôi luôn đăng nhập'"""
        self.login_page.enter_username(config.VALID_USERNAME)
        self.login_page.enter_password(config.VALID_PASSWORD)
        self.login_page.set_remember_me(False)
        
        self.assertFalse(self.login_page.is_remember_me_checked(),
                         "Checkbox 'Giữ tôi luôn đăng nhập' không nên được tích chọn")
        self.login_page.click_login()
        time.sleep(1.5)
        self.login_page.capture_screenshot("TC06_remember_me_unchecked.png")
        
        # Kiểm tra phản hồi thực tế
        error_msg = self.login_page.get_error_message(timeout=3)
        self.assertEqual(error_msg, "", 
                         f"Đăng nhập thất bại: Hệ thống báo '{error_msg}'. "
                         f"(Tài khoản '{config.VALID_USERNAME}' không tồn tại hoặc sai mật khẩu trên máy chủ UTC)")

    def test_tc07_empty_all(self):
        """TC07: Để trống cả Tên đăng nhập và Mật khẩu"""
        self.login_page.enter_username("")
        self.login_page.enter_password("")
        self.login_page.click_login()
        
        error_msg = self.login_page.get_error_message()
        self.login_page.capture_screenshot("TC07_empty_all.png")
        self.assertIn("Bạn chưa nhập tên đăng nhập", error_msg,
                      f"Thông báo lỗi không đúng kỳ vọng. Nhận được: '{error_msg}'")

    # =========================================================================
    # NHÓM 2: GIAO DIỆN & LIÊN KẾT LIÊN QUAN (TC08 - TC10)
    # =========================================================================

    def test_tc08_password_masked(self):
        """TC08: Kiểm tra tính năng ẩn mật khẩu (Masked characters)"""
        is_masked = self.login_page.is_password_masked()
        self.login_page.capture_screenshot("TC08_password_masked.png")
        self.assertTrue(is_masked, "Ô mật khẩu không có thuộc tính type='password'")

    def test_tc09_google_sso_link(self):
        """TC09: Kiểm tra chức năng liên kết 'Đăng nhập bằng e-mail UTC'"""
        google_href = self.login_page.get_google_login_href()
        self.login_page.capture_screenshot("TC09_google_sso.png")
        self.assertTrue("accounts.google.com" in google_href or "oauth2" in google_href,
                        f"Đường dẫn đăng nhập qua Google UTC không hợp lệ: {google_href}")

    def test_tc10_forgot_password_link(self):
        """TC10: Kiểm tra liên kết 'Bạn quên mật khẩu đăng nhập ?'"""
        self.login_page.click_forgot_password()
        time.sleep(1.5)
        
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

    def test_tc11_login_with_enter_key(self):
        """TC11: Đăng nhập bằng cách nhấn phím Enter từ bàn phím"""
        self.login_page.press_enter_on_password("1256")
        time.sleep(1)
        error_msg = self.login_page.get_error_message()
        self.login_page.capture_screenshot("TC11_enter_key.png")
        self.assertIn("Bạn chưa nhập tên đăng nhập", error_msg,
                      f"Nhấn Enter không kích hoạt gửi form kiểm tra: '{error_msg}'")

    def test_tc12_space_only_username(self):
        """TC12: Tên đăng nhập chỉ chứa toàn khoảng trắng (Space-only)"""
        self.login_page.enter_username("   ")
        self.login_page.enter_password("123456")
        self.login_page.click_login()
        time.sleep(1)
        error_msg = self.login_page.get_error_message()
        self.login_page.capture_screenshot("TC12_space_only_username.png")
        self.assertTrue("Tài khoản" in error_msg or "mật khẩu" in error_msg or "chưa nhập" in error_msg,
                        f"Hệ thống không từ chối khoảng trắng hợp lệ. Nhận được: '{error_msg}'")

    def test_tc13_space_only_password(self):
        """TC13: Mật khẩu chỉ chứa toàn khoảng trắng (Space-only)"""
        self.login_page.enter_username("huongnt")
        self.login_page.enter_password("   ")
        self.login_page.click_login()
        time.sleep(1)
        error_msg = self.login_page.get_error_message()
        self.login_page.capture_screenshot("TC13_space_only_password.png")
        self.assertTrue("Tài khoản" in error_msg or "mật khẩu" in error_msg or "chưa nhập" in error_msg,
                        f"Hệ thống không từ chối khoảng trắng hợp lệ. Nhận được: '{error_msg}'")

    def test_tc14_sql_injection(self):
        """TC14: Kiểm tra khả năng chống tấn công SQL Injection cơ bản"""
        self.login_page.enter_username("' OR '1'='1")
        self.login_page.enter_password("123456")
        self.login_page.click_login()
        time.sleep(1)
        error_msg = self.login_page.get_error_message()
        self.login_page.capture_screenshot("TC14_sql_injection.png")
        self.assertTrue("Tài khoản" in error_msg or "mật khẩu" in error_msg,
                        f"Hệ thống xử lý SQL Injection không an toàn: '{error_msg}'")

    def test_tc15_xss_injection(self):
        """TC15: Kiểm tra khả năng chống tấn công XSS Script Injection"""
        self.login_page.enter_username("<script>alert(1)</script>")
        self.login_page.enter_password("123456")
        self.login_page.click_login()
        time.sleep(1)
        error_msg = self.login_page.get_error_message()
        self.login_page.capture_screenshot("TC15_xss_injection.png")
        self.assertTrue("Tài khoản" in error_msg or "mật khẩu" in error_msg,
                        f"Hệ thống xử lý XSS không an toàn: '{error_msg}'")

    def test_tc16_boundary_long_string(self):
        """TC16: Nhập Tên đăng nhập có độ dài cực đại (300 ký tự)"""
        self.login_page.enter_username("a" * 300)
        self.login_page.enter_password("123456")
        self.login_page.click_login()
        time.sleep(1)
        error_msg = self.login_page.get_error_message()
        self.login_page.capture_screenshot("TC16_long_username.png")
        self.assertTrue("Tài khoản" in error_msg or "mật khẩu" in error_msg,
                        f"Hệ thống xử lý chuỗi dài không đúng: '{error_msg}'")

    def test_tc17_special_characters(self):
        """TC17: Tên đăng nhập chứa tập ký tự đặc biệt (!@#$%^&*())"""
        self.login_page.enter_username("admin!@#$%^&*()")
        self.login_page.enter_password("123456")
        self.login_page.click_login()
        time.sleep(1)
        error_msg = self.login_page.get_error_message()
        self.login_page.capture_screenshot("TC17_special_chars.png")
        self.assertTrue("Tài khoản" in error_msg or "mật khẩu" in error_msg,
                        f"Hệ thống xử lý ký tự đặc biệt không đúng: '{error_msg}'")

    def test_tc18_placeholders(self):
        """TC18: Kiểm tra văn bản gợi ý (Placeholder) trên các trường nhập liệu"""
        user_ph = self.login_page.get_username_placeholder()
        pwd_ph = self.login_page.get_password_placeholder()
        self.login_page.capture_screenshot("TC18_placeholders.png")
        self.assertEqual(user_ph, "Tên đăng nhập", f"Placeholder Username không đúng: '{user_ph}'")
        self.assertEqual(pwd_ph, "Mật khẩu", f"Placeholder Password không đúng: '{pwd_ph}'")

    def test_tc19_tab_key_navigation(self):
        """TC19: Kiểm tra điều hướng chuyển con trỏ nhập liệu bằng phím Tab"""
        focused_elem_name = self.login_page.navigate_with_tab_key()
        self.login_page.capture_screenshot("TC19_tab_navigation.png")
        self.assertEqual(focused_elem_name, "userpwd",
                         f"Phím Tab không chuyển focus tới ô mật khẩu (userpwd). Nhận được: '{focused_elem_name}'")

    def test_tc20_footer_links(self):

if __name__ == '__main__':
    unittest.main()
