from selenium.webdriver.firefox.webdriver import WebDriver
from fixture.session import SessionHelper
from fixture.group import GroupHelper


class Application:

    def __init__(self):
        self.wd = WebDriver()
        # self.wd.implicitly_wait(5) needed when page loads dynamically, when element appear on page later
        self.session = SessionHelper(self)
        self.group = GroupHelper(self)

    def is_valid(self):
        try:
            self.wd.current_url
            return True
        except:
            return False

    def open_home_page(self):
        wd = self.wd
        # open page
        wd.get("http://localhost/addressbook/")

    def destroy(self):
        self.wd.quit()
