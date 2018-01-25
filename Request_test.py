"""
    request测试
"""
import requests
import re
import bs4
import lxml
from lxml import etree


def main():
    paras = {
        "jl": "北京",
        "kw": "java开发工程师",
        "sm": 0,
        "isadv": 0,
        "isfilter": 1,
        "p": 1,
        "re": 2006
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3322.4 Safari/537.36',
        'Host': 'sou.zhaopin.com',
        'Connection': 'keep-alive',
        'Referer': 'https://www.zhaopin.com/',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7'
    }
    url = 'https://sou.zhaopin.com/jobs/searchresult.ashx?' 
    r = requests.get(url, headers=headers, params=paras)

    """
        re实现
    """
    # pattern = re.compile('<a style="font-weight: bold".*? target="_blank">(.*?)</a>.*?'
    #     '<td class="gsmc"><a href="(.*?)" target="_blank">(.*?)</a>.*?'
    #     '<td class="zwyx">(.*?)</td>', re.S)
    # items = re.findall(pattern, r.text)
    # for item in items:
    #     print(item[0].replace('<b>', '').replace('</b>', '') + " " + item[1] + " " + item[2] + " " + item[3])
    
    """
        bs4实现
    """
    soup = bs4.BeautifulSoup(r.text, "lxml")
    jobs = soup.find('div', class_='newlist_wrap fl').find('div', class_='newlist_list_content').find_all('table', class_='newlist')
    first_skip = 1
    for job in jobs:
        if first_skip == 1:
            first_skip = 2
            continue
        title = job.find('td', class_='zwmc').a.text
        company = job.find('td', class_='gsmc').a.text
        website = job.find('td', class_='gsmc').a['href']
        salary = job.find('td', class_='zwyx').text
        print(title + " " + company + " " + website + " " + salary)
    """
        xpath实现
    """
    tree = etree.HTML(r.text)
    jobs = tree.xpath(u"//div[@class='newlist_list_content']/table")
    first_skip = 1
    for job in jobs:
        if first_skip == 1:
            first_skip = 2
            continue        
        title = job.xpath(u".//td[contains(@class,'zwmc')]//a/text()")
        if len(title) == 0:
            title = job.xpath(u".//td[contains(@class,'zwmc')]//a/b/text()")
        title = title[0] if len(title) > 0 else 'null'
        company = job.xpath(u".//td[contains(@class,'gsmc')]/a/text()")
        company = company[0] if len(company) > 0 else 'null'
        website = job.xpath(u".//td[contains(@class,'gsmc')]/a/@href")
        website = website[0] if len(website) > 0 else 'null'
        salary = job.xpath(u".//td[contains(@class,'zwyx')]/text()")
        salary = salary[0] if len(salary) > 0 else 'null'
        print(title + " " + company + " " + website + " " + salary)


if __name__ == '__main__':
    main()