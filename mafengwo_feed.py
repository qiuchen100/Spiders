"""
    作者：邱晨
    功能：爬取马蜂窝 http://www.mafengwo.cn/mdd/
"""
import requests
from lxml import etree


def get_html(url):
    """
        获取网页内容并返回
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
        'ContentType': 'text/html; charset=utf-8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
    }
    htmlcontent = requests.get(url, headers=headers, timeout=30)
    htmlcontent.raise_for_status()
    htmlcontent.encoding = "utf-8"
    return htmlcontent.text


def get_all_cities(url):
    """
        获取各个城市
    """
    htmlcontent = get_html(url)
    tree = etree.HTML(htmlcontent)
    mdds = tree.xpath(u"//div[@class='container']//div[@class='wrapper']//div[contains(@class, 'hot-list clearfix')]")
    for mdd in mdds:
        regions = mdd.xpath(u"./div[@class='col']/dl")
        for region in regions:
            print('--------------------------------------------------------------------')
            region_names = region.xpath(u"./dt/a")
            if len(region_names) > 0:
                for region_name in region_names:
                    rname = region_name.xpath(u"./text()")
                    rname = rname[0] if len(rname) > 0 else 'null'
                    rwebsite = region_name.xpath(u"./@href")
                    rwebsite = rwebsite[0] if len(rwebsite) > 0 else 'null'
                    print(rname + " " + rwebsite)

            else:
                region_names =  region.xpath(u"./dt/text()")
                region_names = region_names[0] if len(region_names) > 0 else 'null'
                print(region_names)
            
            cities = region.xpath(u"./dd/a")
            for city in cities:
                    city_name = city.xpath(u"./text()")
                    city_name = city_name[0] if len(city_name) > 0 else 'null'
                    city_website = city.xpath(u"./@href")
                    city_website = city_website[0] if len(city_website) > 0 else 'null'
                    print(city_name + " " + city_website)
            print('--------------------------------------------------------------------')
      


def main():
    url = "http://www.mafengwo.cn/mdd/"
    get_all_cities(url)

if __name__ == '__main__':
    main()

