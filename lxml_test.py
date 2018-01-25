"""
    JD lxml 测试
"""
import lxml
from lxml import html
from lxml import etree
import requests


def get_html(url):
    '''
    封装请求
    '''
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
        'ContentType': 'text/html; charset=utf-8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
    }
    try:
        htmlcontent = requests.get(url, headers=headers, timeout=30)
        htmlcontent.raise_for_status()
        htmlcontent.encoding = 'utf-8'
        return htmlcontent.text
    except:
        return "请求失败"


def main():
    url = "https://item.jd.com/3059256.html"
    html = get_html(url)
    tree = etree.HTML(html)
    print(tree.xpath(u"//*[@class='J-p-3059256']"))

if __name__ == '__main__':
    main()