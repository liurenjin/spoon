from queue import Queue, Empty
from selenium import webdriver

from spoon_server.browser.webdriver_item import WebDriverItem
from spoon_server.browser.webdriver_pool_config import WebDriverPoolConfig


class WebdriverPool(object):
    def __init__(self, config):
        self.config = config
        self.phantomjs_path = config.phantomjs_path
        self.all = Queue()
        self.available = Queue()
        self.stopped = False

    def acquire(self):
        if not self.stopped:
            try:
                return self.available.get_nowait()
            except Empty:
                driver = WebDriverItem(self.config)
                self.all.put(driver)
                return driver.get_webdriver()

    def release(self, driver):
        self.available.put(driver)

    def stop(self):
        self.stopped = True
        while True:
            try:
                driver = self.all.get(block=False)
                driver.get_webdriver().quit()
            except Empty:
                break


if __name__ == "__main__":
    wdp_config = WebDriverPoolConfig(phantomjs_path="D:/program/phantomjs-2.1.1-windows/bin/phantomjs.exe")
    wd = WebdriverPool(wdp_config)
    driver = wd.acquire()
    driver.get("www.baidu.com")
    wd.release(driver)
    wd.stop()
    print(wd.acquire() is None)
