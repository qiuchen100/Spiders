"""
    作者：邱晨
    功能：从http://tianqi.2345.com/获取天气预报
    来源：https://mp.weixin.qq.com/s/flEoqmCQVVFpwJ0zSEonWw
"""
import requests
import lxml
from lxml import etree


def get_html(url):
    '''
    封装请求
    '''
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
        'ContentType': 'text/html; charset=gbk',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
    }
    try:
        htmlcontent = requests.get(url, headers=headers, timeout=30)
        htmlcontent.raise_for_status()
        htmlcontent.encoding = 'gbk'
        return htmlcontent.text
    except:
        return "请求失败"


def get_all_provinces(url):
    htmlcontent = get_html(url)
    tree = etree.HTML(htmlcontent)
    province_urls = tree.xpath(u"//div[@class='clearfix custom']/a/@href")
    province_names = tree.xpath(u"//div[@class='clearfix custom']/a/text()")
    return dict(zip(province_names, province_urls))


def get_all_cities(url):
    htmlcontent = get_html(url)
    tree = etree.HTML(htmlcontent)
    city_urls = tree.xpath(u"//div[@class='citychk']/dl/dt/a/@href")
    city_names = tree.xpath(u"//div[@class='citychk']/dl/dt/a/text()")
    return dict(zip(city_names, city_urls))

def get_city_weather(url):
    htmlcontent = get_html(url)
    tree = etree.HTML(htmlcontent)
    wendu = ""
    wendu_1 = tree.xpath(u"//div[@class='charact']/div[@class='inner']/a/text()")
    wendu = wendu_1[0] if len(wendu_1) > 0 else wendu
    wendu_2 = tree.xpath(u"//div[@class='charact']/div[@class='inner']/a/i/text()")
    wendu = wendu_2[0] if len(wendu_2) > 0 else wendu
    return wendu

def main():
    url = "http://tianqi.2345.com"
    provinces = get_all_provinces(url)
    province_urls = [url + province_url for province_url in provinces.values()]
    for province_url in province_urls:
        cities = get_all_cities(province_url)
        for city_name, city_url in cities.items():
            print(city_name + ": " + url + city_url, end=' ')
            wendu = get_city_weather(url + city_url)
            print("温度: " + wendu)


if __name__ == '__main__':
    main()