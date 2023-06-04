import requests
import json
from bs4 import BeautifulSoup

# 理财信息披露平台主url
base_url = 'https://xinxipilu.chinawealth.com.cn'
# https://xinxipilu.chinawealth.com.cn/Info/6884654

# 产品列表
product_lists_url=[]
# pdf列表
pdf_urls = []
# url和pdf的键值对
url_pdf_dict={}

# 信息披露查询页面
# 可按jgmc请求不同理财公司的报告，后续从bank_list.json中读取所有理财公司列表
# 从业务人员处了解到报告每季度更新一次，plsjStart可取当前日期，plsjEnd往前推3个月或1个月
search_url = base_url + '/lcxpServlet.go?searchFlag=search'
payload = {
    'fbnd': '',
    'cpmc': '',
    'cpfxjg': '',
    'cpdjbm': '',
    'pagenum': '1',
    'pathName': '定期报告',
    'jgmc': '华夏理财有限责任公司',
    'plsjStart': '20230304',
    'plsjEnd': '20230604',
    'method': 'queryBglx'
}
# http头，其实大部分字段不需要的
headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en,zh-CN;q=0.9,zh;q=0.8',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    # 'Content-Length': str(161),
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    # 'Cookie': '_pk_ses.7.c2ce=*; JSESSIONID=2F974F0E77C239DA68C06453BA7D0795; BIGipServerPool_SuperFusion_LiCai_fe_8080=2768503062.36895.0000; BIGipServerPool_SuperFusion_LiCai_Nginx_8080=!abOSVwECepYRUDvDUQsBr01NIeS16b+C8cwGudvL/oDarG1xIz+5GL69KBTue7zc1dBV/Abb53y/XU79ckAnSkKwo5a12cUPKWQgIvqj; _pk_id.7.c2ce=7653877f4364a371.1684930690.3.1685101532.1685101514.',
    'Host': 'xinxipilu.chinawealth.com.cn',
    'Origin': 'https://xinxipilu.chinawealth.com.cn',
    'Pragma': 'no-cache',
    'Referer': 'https://xinxipilu.chinawealth.com.cn/zzlc/jsp/lczzpl/zzplbglx.jsp?bglx=4&num=4',
    'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': f'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}

headers1 = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    # "Cookie": "BIGipServerPool_SuperFusion_LiCai_Nginx_8080=!iTu7eohAQIxWI1MiAKtAGV98KdD1h85z1Bbkltip+otH0VIdoOtaX6OuyUjlZRS+T2wxs3tqmKgjF6U=",
    "Host": "www.chinawealth.com.cn",
    # "If-Modified-Since": "Thu, 18 May 2023 14:37:45 GMT",
    # "If-None-Match": "\"64663839-4071f\"",
    "sec-ch-ua": "\"Microsoft Edge\";v=\"113\", \"Chromium\";v=\"113\", \"Not-A.Brand\";v=\"24\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"macOS\"",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.57"
}

# POST请求信息披露查询页面
response = requests.post(search_url, data=payload, headers=headers)
# 从返回信息中获取产品列表，并将产品列表的url加入product_lists_url
product_lists = json.loads(response.content)['List']
for product_list in product_lists:
    # print(product_list["detailParam"][0]["staticUrl"])
    product_list_url = product_list["detailParam"][0]["staticUrl"]
    product_lists_url.append(product_list_url)
# print(product_lists_url)

# 遍历产品列表product_lists_url，逐条通过GET请求获取相应
# 并将响应的html进行解析，获取其中的pdf文件的url，并将pdf的ulr加入url_pdf_dict字典
# 将字典存入pdf_urls
# 测试 product_lists_url={'/Info/6884940'}
for product_list_url in product_lists_url:
    info_url = base_url + product_list_url
    print(info_url)
    print(info_url)
    response = requests.get(info_url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    # 先找到li标签
    li_elements = soup.find_all('li')
    # 再找到a标签，href是pdf的链接，a标签的文本是pdf名称，用strip去前后空格
    a_element = li_elements[1].find('a')
    url_pdf_dict['pdf_url']=a_element['href']
    url_pdf_dict['pdf_name']=a_element.string.strip()
    print(url_pdf_dict)
    pdf_urls.append(url_pdf_dict)
# print(pdf_urls)

for pdf_url in pdf_urls:
    url = pdf_url['pdf_url']
    name = pdf_url['pdf_name']
    response = requests.get(url, headers=headers1, stream=True)
    try:
        with open(name, 'wb') as f:
            f.write(response.content)
            f.close()
    except:
        f.close()
