"""
    作者：邱晨
    功能：获取天气预报
    来源：https://zhuanlan.zhihu.com/p/30632556
"""
import requests
import bs4


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


def get_content(url):
    '''
    抓取页面天气数据
    '''
    weather_list = []
    html = get_html(url)
    soup = bs4.BeautifulSoup(html, "lxml")
    content_ul = soup.find('div', class_='t').find('ul', class_='clearfix').find_all('li', recursive=False) # recursive=False 表示只搜索子节点，不会搜索下面的孙节点
    for content in content_ul:
        try:
            weather = {}
            weather["日期"] = content.find('h1').text
            weather["空气状况"] = content.find('p', class_='wea').text
            weather["温度"] = content.find('p', class_='tem').find('span').text + content.find('p', class_='tem').find('em').text
            weather_list.append(weather)
        except:
            print(content.text)
    print(weather_list)


def main():
    url = "http://www.weather.com.cn/weather1d/101280101.shtml#dingzhi_first"
    get_content(url)


if __name__ == '__main__':
    main()
