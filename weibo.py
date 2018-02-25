"""
    作者：邱晨
    功能：爬取微博数据
"""
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import requests
import time
from selenium.webdriver.common.by import By

user_agent = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) " +
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36"
)

dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.userAgent"] = user_agent

feeds_crawler = webdriver.PhantomJS(desired_capabilities=dcap, executable_path=r'C:\Users\qiuc\AppData\Roaming\npm\phantomjs.cmd')
feeds_crawler.set_window_size(1920, 1200)  # optional

url_home = 'https://weibo.com'
seed_user = 'https://weibo.com/528545660'

def get_html(url):
    feeds_crawler.get(url)
    time.sleep(5)
    es = feeds_crawler.find_elements_by_xpath('//span[contains(@class,"S_txt1 t_link")]')
    for e in es:
        print(e.text)

def login(username, password):
    feeds_crawler.get(url_home)
    time.sleep(5)
    print(feeds_crawler.current_url)
    feeds_crawler.find_element_by_id('loginname').send_keys(username)
    feeds_crawler.find_element_by_name('password').send_keys(password)
    # btn = feeds_crawler.find_elements_by_xpath('//div[contains(@class,"login_btn")]/a')
    # btn = feeds_crawler.find_element(By.XPATH, '//a[@class="W_btn_a btn_32px "]')
    print(feeds_crawler.)                                   
    btn.click()

def main():
    username = '18665866991'
    password = 'tcl8469375'
    login(username, password)
    # get_html(seed_user)
    feeds_crawler.close()

if __name__ == '__main__':
    main()