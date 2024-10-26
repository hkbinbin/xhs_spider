from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import base64
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt

# 创建 WebDriver
service = Service(executable_path="/home/hkbin/.cargo/bin/geckodriver")  # 替换为 geckodriver 的路径
driver = webdriver.Firefox(service=service)

def login():
# 打开页面
    driver.get("https://www.xiaohongshu.com/explore")
    try:
        # 等待 class="qrcode-img" 元素加载完成（最多等待5秒）
        qrcode_element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "qrcode-img"))
        )
        qrcode_src = qrcode_element.get_attribute("outerHTML")
        print("找到的二维码元素HTML：", qrcode_src)
        key_str = 'src="data:image/png;base64,'
        offset = qrcode_src.find(key_str)
        end = qrcode_src.find('">', offset)
        qrcode_base64 = qrcode_src[offset + len(key_str):end]
        image_data = base64.b64decode(qrcode_base64)
        image = Image.open(BytesIO(image_data))
        # 展示二维码图片
        plt.imshow(image)
        plt.axis('off')  # 关闭坐标轴
        plt.show() # 会阻塞掉
    except Exception as e:
        print("未找到二维码元素:", e)

def spider_user(profile_id): # 5f7050f4000000000100664c
    url = 'https://www.xiaohongshu.com/user/profile/' + profile_id
    driver.get(url)
    # try roll
    try:
        time.sleep(0.5)

        scroll_pause_time = 0.5  # 每次滚动后等待的时间
        last_height = driver.execute_script("return document.body.scrollHeight")

        hrefs = set()
        while True:
            # 向下滚动
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # 等待页面加载
            time.sleep(scroll_pause_time)
            # 计算新的高度并与旧高度进行比较
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
            elements = WebDriverWait(driver, 1).until(
                lambda d: d.find_elements(By.CSS_SELECTOR, ".cover.ld.mask")
            )
            print(len(elements))
            # 输出元素的文本和属性
            for element in elements:
                href = element.get_attribute('href')
                print(f"href: {href}")
                hrefs.add(href)
        
        print(len(hrefs))
        # for href_url in iter(hrefs):
        #     print(href_url)
    except Exception as e:
        print("spider_user error: ", e)

def main():
    login()
    spider_user("5f7050f4000000000100664c")



if __name__ == "__main__":
    main()


driver.quit()

# 循环添加所有 cookies
# for cookie in cookies:
#     driver.add_cookie(cookie)

# 刷新页面以应用 cookie
# driver.refresh()



# # 注入 JavaScript，拦截 console.log 并存储日志
# driver.execute_script("""
#     (function() {
#         const logs = [];
#         const oldLog = console.log;
#         console.log = function(...args) {
#             // 将每个参数转换为 JSON 字符串
#             const jsonArgs = args.map(arg => {
#                 try {
#                     return JSON.stringify(arg);
#                 } catch (e) {
#                     return String(arg);  // 如果不能转换，则转为字符串
#                 }
#             });
#             logs.push(jsonArgs.join(' '));  // 将日志保存到数组中
#             oldLog.apply(console, args);
#         };
#         window.getLogs = () => logs;  // 暴露一个函数来获取日志
        
#         // 将 rt 函数暴露到全局对象
#         window.rt = function() {
#             let t = "";
#             for (let e = 0; e < 16; e++)
#                 t += "abcdef0123456789".charAt(Math.floor(16 * Math.random()));
#             return t;
#         };
#     })();
# """)

# 等待页面加载
# time.sleep(0.5)

# scroll_pause_time = 0.5  # 每次滚动后等待的时间
# last_height = driver.execute_script("return document.body.scrollHeight")

# while True:
#     # 向下滚动
#     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#     # 等待页面加载
#     time.sleep(scroll_pause_time)
#     # 计算新的高度并与旧高度进行比较
#     new_height = driver.execute_script("return document.body.scrollHeight")
#     if new_height == last_height:
#         break
#     last_height = new_height


# # 获取页面的所有内容
# page_content = driver.page_source

# # 打印或解析页面内容
# # print(page_content)


# with open("./save.txt", "w") as file:
#     file.write(page_content)


# import json
# x_s_t = json.loads(logs[0])
# X_s = x_s_t["X-s"]
# X_t = str(x_s_t["X-t"])

# print("X-s: ", x_s_t["X-s"])
# print("X-t: ", x_s_t["X-t"])

# print("X-b3-traceid: ", logs[1].strip('"'))

# x8 = "I38rHdgsjopgIvesdVwgIC+oIELmBZ5e3VwXLgFTIxS3bqwErFeexd0ekncAzMFYnqthIhJeSBMDKutRI3KsYorWHPtGrbV0P9WfIi/eWc6eYqtyQApPI37ekmR1QL+5Ii6sdnoeSfqYHqwl2qt5B0DoIvMzOZQqZVw7IxOeTqwr4qtiIkrOIi/skccxICLdI3Oe0utl2ADZsLveDSKsSPw5IEvsiutJOqw8BVwfPpdeTDWOIx4VIiu6ZPwbPut5IvlaLbgs3qtxIxes1VwHIkumIkIyejgsY/WTgeAsjutKrZgedWI9gfKeYIHPI3ge0VtZIk3edqtAmzPjNgDHIxOekPtR/WOex0lyIhYsIE8+qoqjICuPqYGnIiciePt5ICZC4BNsDces6uw1IvKef9de00znIiAe1Mi7yuwuIiKeTf0sxz/e1Vt4ZdvsdutWIxiem9AsdqtEssKsWVw8IxI2I383sqwZgVtQa7zLwLOsD0OexutmIk6eYa/sxpI1IkosWL6sxfhuIk7e6utdIkqIQqwHtPtAI33e1qtWIkNs1VwDIEKsfqtltqwseqwlIvqAIxDc8nqiKWJeiqtIIEq8Ii7eSPw4bzmynjOsWUmdIiPyqPttZPwlIvAexVtjODAeVY5sVLzLIE0s6edsiqt8cPwrICJsWutfIEvsTgDPIkvs173sSPwXIC5e3PwDt9YaIhQgIvNs1p6e6gve0MgsdVtmIiPRI3SEoPtLIC8EIh6skbF3+A/eWutbIE82eut12zAsYzgeWPwboPwGIvZ4ICVyoI=="
# o = X_t + '_' + X_s
# i = X_t
# c = X_t
# l = X_s
# h = x8

# driver.execute_script(f"""
#     console.log(encrypt_mcr(concat_default()(
#         o = concat_default()(
#             i = "".concat("{c}")
#         ).call("{i}", "{l}")
#     ).call("{o}", "{h}")));
# """)
# driver.execute_script(f"""
#     console.log(encrypt_b64Encode);

# """)

# logs = driver.execute_script("return window.getLogs();")
# print(logs[0])

"""
{
    "s0": 5, // 定值
    "s1": "", // 定值
    "x0": "1", // 定值
    "x1": "3.6.8", // 定值
    "x2": "Windows", // 定值
    "x3": "xhs-pc-web", // 定值
    "x4": "4.21.0", // 定值
    "x5": "18ee0b8eaa14szquw6otb9amxbdj35n5nrhcpqi4j50000360507", // a1 的值 cookie里的a1
    "x6": 1718762991893,  // x-t 的值
    // x-s 的值
    "x7":"XYW_eyJzaWduU3ZuIjoiNTEiLCJzaWduVHlwZSI6IngxIiwiYXBwSWQiOiJ4aHMtcGMtd2ViIiwic2lnblZlcnNpb24iOiIxIiwicGF5bG9hZCI6ImQ4M2I2NTY0OTY2ZGQzZDdmYzRlNzM0NTA5M2VlM2U1ZWRiZjc0NjcyMDExOTI5OGU0YjBjMzE1Zjg2MTI0ZDFhMTc4NGQ1NGY4MDc1NWY2NzQzODhlNGU5MGRkYTVkYmM5ZTNiZmRhMWZhYTFlYjkwZDc0YWEzMWI1NGM3MmNkMGQ3NGFhMzFiNTRjNzJjZGFjNDg5YjlkYThjZTVlNDhmNGFmYjlhY2ZjM2VhMjZmZTBiMjY2YTZiNGNjM2NiNTFiYzdiMDlhMTBjNjliZDQzYjgxNTY5ZWQ1ZWRmNjlhYWQ4OGU5MTRiZWY4ZjE3NTVjMzMwYjA2ZGI5YmY3YjAwM2EwZGIxMDhmMTk3OTgyM2I2OGUxNzE5MWRmM2NhZmUzN2YxM2RkZWVjZDJmMTk4YWFkYzBmNmE2MGFjNWVmNjkyODNhZTcwMGYyMWRmOTBkYWMyOTA5NjNlMTRkZWY4YTBlMTEzMjMwYzE3MWQ4NzE4ZGNlOTkwNTkzODkzMSJ9",
    // 浏览器指纹，可以写死
    "x8": "I38rHdgsjopgIvesdVwgIC+oIELmBZ5e3VwXLgFTIxS3bqwErFeexd0ekncAzMFYnqthIhJeSBMDKutRI3KsYorWHPtGrbV0P9WfIi/eWc6eYqtyQApPI37ekmR1QL+5Ii6sdnoeSfqYHqwl2qt5B0DoIvMzOZQqZVw7IxOeTqwr4qtiIkrOIi/skccxICLdI3Oe0utl2ADZsLveDSKsSPw5IEvsiutJOqw8BVwfPpdeTDWOIx4VIiu6ZPwbPut5IvlaLbgs3qtxIxes1VwHIkumIkIyejgsY/WTgeAsjutKrZgedWI9gfKeYIHPI3ge0VtZIk3edqtAmzPjNgDHIxOekPtR/WOex0lyIhYsIE8+qoqjICuPqYGnIiciePt5ICZC4BNsDces6uw1IvKef9de00znIiAe1Mi7yuwuIiKeTf0sxz/e1Vt4ZdvsdutWIxiem9AsdqtEssKsWVw8IxI2I383sqwZgVtQa7zLwLOsD0OexutmIk6eYa/sxpI1IkosWL6sxfhuIk7e6utdIkqIQqwHtPtAI33e1qtWIkNs1VwDIEKsfqtltqwseqwlIvqAIxDc8nqiKWJeiqtIIEq8Ii7eSPw4bzmynjOsWUmdIiPyqPttZPwlIvAexVtjODAeVY5sVLzLIE0s6edsiqt8cPwrICJsWutfIEvsTgDPIkvs173sSPwXIC5e3PwDt9YaIhQgIvNs1p6e6gve0MgsdVtmIiPRI3SEoPtLIC8EIh6skbF3+A/eWutbIE82eut12zAsYzgeWPwboPwGIvZ4ICVyoI==",
    "x9": -1854331133,
    // 请求次数，可以写死
    "x10": 22
}    


"""

# cookie = {
#     "Cookie": "abRequestId=40d51d83-7f98-5f74-98fd-0e01ceded871",
#     "webBuild": "4.38.0",
#     "a1": "1928eb57f0bm53l600cu762cekf5krziooomxq4zb50000158734",
#     "webId": "d494a83d86e22a87553fca13f0fc1e10", 
#     "gid": "yjJYdD2Yi8ldyjJYdD2WilA48D62q1K88S7WluDKJSdTi6282TFu3C888y2YWq48y82jiYY0",
#     "xsecappid": "xhs-pc-web", 
#     "web_session": "040069b67a4223225d24785c3b354bf67fd409",
#     "unread": "{%22ub%22:%2266f15cc9000000002c017847%22%2C%22ue%22:%2266f92673000000001b02014c%22%2C%22uc%22:33}",
#     "acw_tc": "21d335e62cd7347d1750531027ed7a4e0211f742b01da185b662bbb1832c0988",
#     "websectiga": "cffd9dcea65962b05ab048ac76962acee933d26157113bb213105a116241fa6c",
#     "sec_poison_id": "3e57f46d-9e41-4022-b9b6-d9970765ce61",
# }

# driver.add_cookie(cookie)

# driver.get("https://edith.xiaohongshu.com/api/sns/web/v1/user_posted?num=30&cursor=66e04343000000001e01b21c&user_id=66c2e6fc000000001d030738&image_formats=jpg,webp,avif")

# title = driver.title

# print(title)


# 关闭浏览器

# import requests

# headers = {
#     "X-b3-traceid": logs[1].strip('"'),
#     "X-s": x_s_t["X-s"],
#     "X-t": str(x_s_t["X-t"]),
# }
# url = "https://edith.xiaohongshu.com/api/sns/web/v1/user_posted?num=30&cursor=66e04343000000001e01b21c&user_id=66c2e6fc000000001d030738&image_formats=jpg,webp,avif"

# resp = requests.get(url=url, headers = headers)

# print(resp.text)
# print(resp.request.headers)


# driver.quit()
