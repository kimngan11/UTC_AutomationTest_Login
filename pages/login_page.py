import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pages.base_page import BasePage
import config

class LoginPage(BasePage):
    """
    Page Object Model cho trang Đăng nhập Văn phòng điện tử UTC
    Kế thừa từ BasePage.
    URL: https://vanphongdientu.utc.edu.vn/Login
    """

    # Locators các phần tử trên trang đăng nhập UTC
    LOCATOR_USERNAME = (By.NAME, "username")
    LOCATOR_PASSWORD = (By.NAME, "userpwd")
    LOCATOR_REMEMBER_ME = (By.ID, "persistent")
    LOCATOR_REMEMBER_LABEL = (By.CSS_SELECTOR, "label[for='persistent'], label.check")
    LOCATOR_SUBMIT_BUTTON = (By.CSS_SELECTOR, "input.submit_login")
    LOCATOR_ERROR_MESSAGE = (By.CSS_SELECTOR, "div.error")
    LOCATOR_GOOGLE_LOGIN = (By.LINK_TEXT, "Đăng nhập bằng e-mail UTC")
    LOCATOR_FORGOT_PASSWORD = (By.LINK_TEXT, "Bạn quên mật khẩu đăng nhập ?")
    LOCATOR_HELP_CENTER = (By.LINK_TEXT, "Trung tâm trợ giúp")
    LOCATOR_FEEDBACK = (By.LINK_TEXT, "Ý kiến phản hồi")

    def __init__(self, driver):
        super().__init__(driver)

    def open(self):
        """Mở trang đăng nhập UTC"""
        self.open_url(config.BASE_URL)
        return self

    def enter_username(self, username: str):
        """Nhập tên đăng nhập"""
        self.enter_text(self.LOCATOR_USERNAME, username)
        return self

    def enter_password(self, password: str):
        """Nhập mật khẩu"""
        self.enter_text(self.LOCATOR_PASSWORD, password)
        return self

    def press_enter_on_password(self, password: str = ""):
        """Nhập mật khẩu và nhấn phím Enter để kích hoạt submit form"""
        pwd_elem = self.enter_text(self.LOCATOR_PASSWORD, password)
        pwd_elem.send_keys(Keys.ENTER)
        return self

    def set_remember_me(self, should_check: bool = True):
        """
        Tích hoặc bỏ tích checkbox 'Giữ tôi luôn đăng nhập'.
        Do jQuery ẩn input checkbox gốc và chèn custom label,
        sử dụng execute_script để click an toàn và chính xác.
        """
        checkbox = self.find_element(self.LOCATOR_REMEMBER_ME)
        is_currently_checked = checkbox.is_selected()

        if should_check != is_currently_checked:
            self.execute_script("arguments[0].click();", checkbox)
        return self

    def is_remember_me_checked(self) -> bool:
        """Kiểm tra checkbox Giữ tôi luôn đăng nhập có đang được chọn hay không"""
        checkbox = self.find_element(self.LOCATOR_REMEMBER_ME)
        return checkbox.is_selected()

    def click_login(self):
        """Click vào nút Đăng nhập"""
        self.click(self.LOCATOR_SUBMIT_BUTTON)
        return self

    def login(self, username: str, password: str, remember_me: bool = False):
        """Thực hiện quy trình đăng nhập hoàn chỉnh"""
        self.enter_username(username)
        self.enter_password(password)
        self.set_remember_me(remember_me)
        self.click_login()
        return self

    def get_error_message(self, timeout: int = 5) -> str:
        """Lấy nội dung thông báo lỗi trên trang nếu có"""
        return self.get_text(self.LOCATOR_ERROR_MESSAGE, timeout=timeout)

    def is_password_masked(self) -> bool:
        """Kiểm tra ô mật khẩu có thuộc tính type='password' (ẩn ký tự) không"""
        return self.get_attribute(self.LOCATOR_PASSWORD, "type") == "password"

    def get_username_placeholder(self) -> str:
        """Lấy văn bản gợi ý (placeholder) của ô Tên đăng nhập"""
        return self.get_attribute(self.LOCATOR_USERNAME, "placeholder")

    def get_password_placeholder(self) -> str:
        """Lấy văn bản gợi ý (placeholder) của ô Mật khẩu"""
        return self.get_attribute(self.LOCATOR_PASSWORD, "placeholder")

    def navigate_with_tab_key(self) -> str:
        """Nhấn phím Tab từ ô Username và trả về name của phần tử được focus"""
        user_elem = self.find_element(self.LOCATOR_USERNAME)
        user_elem.click()
        user_elem.send_keys(Keys.TAB)
        active_element = self.driver.switch_to.active_element
        return active_element.get_attribute("name") or active_element.get_attribute("id") or ""

    def get_google_login_href(self) -> str:
        """Lấy URL chuyển tiếp của nút 'Đăng nhập bằng e-mail UTC'"""
        return self.get_attribute(self.LOCATOR_GOOGLE_LOGIN, "href")

    def click_google_login(self):
        """Click vào nút Đăng nhập bằng e-mail UTC"""
        self.click(self.LOCATOR_GOOGLE_LOGIN)
        return self

    def click_forgot_password(self):
        """Click vào liên kết Quên mật khẩu"""
        self.click(self.LOCATOR_FORGOT_PASSWORD)
        return self

    def get_help_center_href(self) -> str:
        """Lấy href của liên kết 'Trung tâm trợ giúp' ở chân trang"""
        return self.get_attribute(self.LOCATOR_HELP_CENTER, "href")

    def get_feedback_href(self) -> str:
        """Lấy href của liên kết 'Ý kiến phản hồi' ở chân trang"""
        return self.get_attribute(self.LOCATOR_FEEDBACK, "href")
