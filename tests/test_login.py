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

if __name__ == '__main__':
    unittest.main()
