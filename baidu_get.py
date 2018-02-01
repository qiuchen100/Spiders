"""
    作者：邱晨
    功能：自学用selenium+PHANTOMJS搜索百度
    来源：https://zhuanlan.zhihu.com/p/27115580
"""
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import requests
import time

user_agent = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) " +
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36"
)

dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.userAgent"] = user_agent

browser = webdriver.PhantomJS(desired_capabilities=dcap, executable_path=r'C:\Users\qiuc\AppData\Roaming\npm\phantomjs.cmd')
browser.set_window_size(1920, 1200)  # optional

url = 'https://www.baidu.com/'

def get_Content():
    """
        获取搜索内容
    """
    results = browser.find_elements_by_class_name('t')
    for result in results:
        print('标题：{}超链接：{}'.format(result.text, result.find_element_by_tag_name('a').get_attribute('href'))) 
    else:
        print('----------------------------------------------------------------------------------------')   

def main():
    browser.get(url)
    browser.implicitly_wait(3)
    text = browser.find_element_by_id('kw')
    text.send_keys('python')  # 可以输入你自己想要搜索的内容
    browser.find_element_by_id('su').submit()
    get_Content()
    for i in range(2):
        next_btn = browser.find_element_by_class_name('n')
        browser.get(next_btn.get_attribute('href'))
        browser.implicitly_wait(3)
        get_Content()


if __name__ == '__main__':
    main()