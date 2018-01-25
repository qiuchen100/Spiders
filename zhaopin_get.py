"""
    功能：抓取智联招聘基础版
    来源：https://mp.weixin.qq.com/s/_wBoWK8gN9I1DwvBdo3PCw
"""
import re
import requests
from urllib.parse import urlencode
import csv

def get_one_page(city, keyword, region, page):
    """
        获取网页内容并返回
    """
    paras = {
        "jl": city,
        "kw": keyword,
        "sm": 0,
        "p": page,
        "re": region
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

    url = 'https://sou.zhaopin.com/jobs/searchresult.ashx?' + urlencode(paras)
    try:
        htmlcontent = requests.get(url, headers=headers, timeout=30)
        htmlcontent.raise_for_status()
        htmlcontent.encoding = 'utf-8'
        return htmlcontent.text
    except:
        return "请求失败"

def parse_one_page(html):
    """
        解析html代码
    """
    pattern = re.compile('<a style=.*? target="_blank">(.*?)</a>.*?'        # 匹配职位信息
        '<td class="gsmc"><a href="(.*?)" target="_blank">(.*?)</a>.*?'     # 匹配公司网址和公司名称
        '<td class="zwyx">(.*?)</td>', re.S)                                # 匹配月薪  
        # <a style="font-weight: bold" par="ssidkey=y&amp;ss=201&amp;ff=03&amp;sg=16ad20e81df84ab7a9e48177eb8f9dd7&amp;so=1" href="http://jobs.zhaopin.com/329792939250052.htm" target="_blank">量化算法工程师（Python中级）</a>
        # <td class="gsmc"><a href="http://company.zhaopin.com/CC329792939.htm" target="_blank">云量科技(北京)有限责任公司</a> <a href="http://company.zhaopin.com/CC329792939.htm" target="_blank" style="vertical-align: top;"><img src="//img03.zhaopin.cn/IHRNB/img/souvip1002.png" border="0" align="absmiddle" alt="1002" class="icon_vip"></a></td>
        # <td class="zwyx">10001-15000</td>
    items = re.findall(pattern, html)
    for item in items:
        job_name = item[0]
        job_name = job_name.replace('<b>', '')
        job_name = job_name.replace('</b>', '')
        yield {
            'job': job_name,
            'website': item[1],
            'company': item[2],
            'salary': item[3]
        }


# def write_csv_file(path, headers, rows):
#     '''
#     将表头和行写入csv文件
#     '''
#     # 加入encoding防止中文写入报错
#     # newline参数防止每写入一行都多一个空行
#     with open(path, 'a', encoding='gb18030', newline='') as f:
#         f_csv = csv.DictWriter(f, headers)
#         f_csv.writeheader()
#         f_csv.writerows(rows)

def write_csv_headers(path, headers):
    '''
    写入表头
    '''
    with open(path, 'a', encoding='gb18030', newline='') as f:
        f_csv = csv.DictWriter(f, headers)
        f_csv.writeheader()

def write_csv_rows(path, headers, rows):
    '''
    写入行
    '''
    with open(path, 'a', encoding='gb18030', newline='') as f:
        f_csv = csv.DictWriter(f, headers)
        f_csv.writerows(rows) 

def main():
    '''
    主函数
    '''
    city = '北京'
    keyword = 'python工程师'
    region = 2006
    pages = 3
    filename = 'zl_' + city + '_' + keyword + '.csv'
    headers = ['job', 'website', 'company', 'salary']
    write_csv_headers(filename, headers)
    for i in range(1, pages):
        '''
        获取该页中所有职位信息，写入csv文件
        '''
        jobs = []
        html = get_one_page(city, keyword, region, i)
        items = parse_one_page(html)
        for item in items:
            jobs.append(item)
        write_csv_rows(filename, headers, jobs)

if __name__ == '__main__':
    main()