import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import config

class BasePage:
    """
    Lớp cha BasePage đóng gói các hàm thao tác chung với Selenium WebDriver.
    Tất cả các Page Object (ví dụ LoginPage) đều kế thừa từ lớp này.
    """

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, config.EXPLICIT_WAIT)

    def open_url(self, url: str):
        """Mở một trang web theo URL"""
        self.driver.get(url)
        return self

    def find_element(self, locator: tuple, timeout: int = None):
        """Tìm một phần tử hiển thị trên trang có áp dụng Explicit Wait"""
        wait = WebDriverWait(self.driver, timeout) if timeout else self.wait
        return wait.until(EC.presence_of_element_located(locator))

    def find_visible_element(self, locator: tuple, timeout: int = None):
        """Tìm một phần tử có hiển thị trực quan (visible) trên trang"""
        wait = WebDriverWait(self.driver, timeout) if timeout else self.wait
        return wait.until(EC.visibility_of_element_located(locator))

    def click(self, locator: tuple, timeout: int = None):
        """Chờ phần tử có thể click được và click"""
        wait = WebDriverWait(self.driver, timeout) if timeout else self.wait
        element = wait.until(EC.element_to_be_clickable(locator))
        element.click()
        return element

    def enter_text(self, locator: tuple, text: str, clear_first: bool = True):
        """Nhập dữ liệu văn bản vào ô input"""
        element = self.find_element(locator)
        if clear_first:
            element.clear()
        if text:
            element.send_keys(text)
        return element

    def get_text(self, locator: tuple, timeout: int = 5) -> str:
        """Lấy văn bản hiển thị của phần tử"""
        try:
            element = self.find_visible_element(locator, timeout=timeout)
            return element.text.strip()
        except Exception:
            return ""

    def get_attribute(self, locator: tuple, attribute_name: str) -> str:
        """Lấy giá trị của một thuộc tính HTML bất kỳ"""
        element = self.find_element(locator)
        return element.get_attribute(attribute_name) or ""

    def execute_script(self, script: str, *args):
        """Thực thi đoạn mã JavaScript trên trình duyệt"""
        return self.driver.execute_script(script, *args)

    def get_current_url(self) -> str:
        """Lấy URL hiện tại của trình duyệt"""
        return self.driver.current_url

    def get_title(self) -> str:
        """Lấy tiêu đề trang hiện tại"""
        return self.driver.title

    def capture_screenshot(self, filename: str) -> str:
        """Chụp ảnh màn hình lưu vào thư mục screenshots"""
        os.makedirs(config.SCREENSHOT_DIR, exist_ok=True)
        filepath = os.path.join(config.SCREENSHOT_DIR, filename)
        self.driver.save_screenshot(filepath)
        return filepath
