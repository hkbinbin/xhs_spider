import requests
from bs4 import BeautifulSoup

login_url = "https://edith.xiaohongshu.com/api/sns/web/v2/login/send_code?phone=15089713927&zone=86&type=login"

# json_data = {"clientTime":1728973696099,"context_sdkSessionId":"d4d001e5-5d3e-4819-ac4d-091cf9d3581c","context_pageSessionId":"58dd0a0a-20bb-4639-8575-56745c9f1711","context_sdkSeqId":236,"context_nameTracker":"wapT","context_platform":"PC","context_appVersion":"discovery-undefined","context_osVersion":"unknown","context_deviceModel":"","context_deviceId":"415764dd0d3f7ab605d735f875d7d102","context_package":"","context_networkType":"unknow","context_matchedPath":"/explore/:noteId","context_route":"https://www.xiaohongshu.com/explore/66dd2a5500000000260317a3?xsec_token=ABWlE5aUHic0mmdjIn0CX-sfgfXKCMUCcDbB7szI3Y-CM=&xsec_source=pc_feed","context_userAgent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:130.0) Gecko/20100101 Firefox/130.0","context_artifactName":"xhs-pc-web","context_artifactVersion":"4.38.0","context_networkQuality":"GOOD","context_deviceLevel":"1","context_userId":"670e034d000000001b019075","measurement_name":"httpRequestTiming","measurement_data":{"method":"GET","matchedPath":"/api/sns/web/v2/login/send_code","status":0,"errorType":"HTTPClientError","traceId":"98408375aaf0d033","url":"//edith.xiaohongshu.com/api/sns/web/v2/login/send_code?phone=15089713927&zone=86&type=login","errorMsg":"Network Error","apiPrefetchType":5,"code":"ERR_NETWORK","isRiskUser":"risk","isRiskReason":"[\"PluginPrototype\",\"AudioCodecs\"]","i12":16,"i13":0,"i14":0,"ext1":"normal"}}
# headers = {
#     "Host": "apm-fe.xiaohongshu.com",
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:130.0) Gecko/20100101 Firefox/130.0",
#     "Accept": "*/*",
#     "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
#     "Accept-Encoding": "gzip, deflate, br, zstd",
#     "Referer": "https://www.xiaohongshu.com/",
#     "content-type": "application/json",
#     "Biz-Type": "apm_fe",
#     "Batch": "false",
#     "Content-Length": "1384",
#     "Origin": "https://www.xiaohongshu.com",
#     "DNT": "1",
#     "Connection": "keep-alive",
#     "Sec-Fetch-Dest": "empty",
#     "Sec-Fetch-Mode": "cors",
#     "Sec-Fetch-Site": "same-site",
#     "Priority": "u=4"
# }

resp = requests.options(url = login_url)
print(resp.text)

"""
# login first to get cookie 
resp = requests.get("https://www.xiaohongshu.com/explore/66dd2a5500000000260317a3")

soup = BeautifulSoup(resp.text, 'html.parser')
# print(soup.prettify())

header = soup.head

description = header.find('meta', attrs={'name': 'description'})
keywords = header.find('meta', attrs={'name': 'keywords'})
title = header.find('meta', attrs={'name': 'og:title'})
images = header.find_all('meta', attrs={'name': 'og:image'})

print("description: ", description)
print("keywords: ", keywords)
print("title: ", title)
print("images: ", images)

### next is comment
print(soup.body)

"""