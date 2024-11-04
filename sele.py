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
# database
import sqlite3

def log_text(text):
    print(f"\033[1;32m[*] {text}\033[0m\n")


def log_hex(value):
    print(f"\033[1;33m[+] 0x{value}\033[0m\n")


def log_error(text):
    print(f"\033[1;31m[x] {text}\033[0m\n")


# 创建 WebDriver
service = Service(executable_path="/snap/bin/geckodriver")  # !替换为 geckodriver 的路径

options = Options()

ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0'
options.set_preference('general.useragent.override', ua)
options.add_argument("--headless")

driver = webdriver.Firefox(service=service, options=options)

file = open("log.txt", "w")

def connect_database():
    # create database
    conn = sqlite3.connect('xhs.db')  # 'example.db' 是数据库文件名
    return conn

def create_table(conn):
    cursor = conn.cursor()
    # create table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_keywords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            xhs_id TEXT NOT NULL UNIQUE,
            ip TEXT NOT NULL,
            intro TEXT NOT NULL,
            key_words TEXT NOT NULL
        )
    ''')

    conn.commit()


def insert_data(conn, username, xhs_id, ip, intro, key_words):
    cursor = conn.cursor()
    
    # Check if user exists
    cursor.execute('SELECT key_words FROM user_keywords WHERE xhs_id = ?', (xhs_id,))
    user = cursor.fetchone()

    if user:
        # 如果用户存在，先获取当前的 key_words
        existing_key_words = user[0]  # 提取现有的 key_words

        updated_key_words = existing_key_words + key_words

        # 更新用户数据
        cursor.execute('''
            UPDATE user_keywords
            SET username = ?, ip = ?, key_words = ?
            WHERE xhs_id = ?
        ''', (username, ip, updated_key_words, xhs_id))
    else:
        # 用户不存在，插入新用户
        cursor.execute('''
            INSERT INTO user_keywords (username, xhs_id, ip, intro, key_words)
            VALUES (?, ?, ?, ?, ?)
        ''', (username, xhs_id, ip, intro, key_words))

    conn.commit()


def log_write(text):
    file.write(text)
    file.flush()

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

def spider_user(profile_id, conn): # 5f7050f4000000000100664c
    user_data = [] # * for database
    url = 'https://www.xiaohongshu.com/user/profile/' + profile_id
    driver.get(url)
    # try roll
    try:
        # *get username & id & ip
        username = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "user-name"))
        ).text
        log_text("username: " + username)
        user_data.append(username)

        xhs_id = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "user-redId"))
        ).text
        log_text("userid: " + xhs_id)
        user_data.append(xhs_id)

        ip = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "user-IP"))
        ).text
        log_text("ip: " + ip)
        user_data.append(ip)

        # *get intro
        intro = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "user-desc"))
        ).text
        log_text("intro: " + intro)
        user_data.append(intro)

        # conn, username, xhs_id, ip, intro, key_words
        insert_data(conn, username, xhs_id, ip, intro, "") # ! init a user

        scroll_pause_time = 0.3  # 每次滚动后等待的时间
        last_height = driver.execute_script("return document.body.scrollHeight")

        hrefs = set()
        while True:
            elements = WebDriverWait(driver, 1).until(
                lambda d: d.find_elements(By.CSS_SELECTOR, ".cover.ld.mask")
            )
            print(len(elements))
            # 输出元素的文本和属性
            for element in elements:
                href = element.get_attribute('href')
                print(f"href: {href}")
                hrefs.add(href)
            # 向下滚动
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # 等待页面加载
            time.sleep(scroll_pause_time)
            # 计算新的高度并与旧高度进行比较
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height        
        print(len(hrefs))

        return hrefs, user_data
        # for href_url in iter(hrefs):
        #     print(href_url)
    except Exception as e:
        print("spider_user error: ", e)

def get_post(i, url, dic):
    driver.get(url)
    log_text("note order: " + str(i))
    # ?get all
    # *get title first
    title = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "title"))
    ).text
    log_text("Get title: " + title)
    log_write("---Title: " + title + "\n")
    # *get note-text
    note_text = driver.find_element(By.CSS_SELECTOR, ".note-text span").text
    log_text("note:"+ note_text)
    log_write("-----note: " + note_text + "\n")
    # *get tag
    wtags = ""
    tags = driver.find_elements(By.CSS_SELECTOR, "a.tag")
    for tag in tags:
        log_text("Tag: "+ tag.text)
        wtags += tag.text + " "
        # judge if has keys
        if(dic.get(tag.text)):
            dic[tag.text] += 1
        else:
            dic[tag.text] = 1
    log_write("-----tags: " + wtags + "\n")

def main():
    log_text("prepare to login")
    login()
    log_text("prepare database")
    conn = connect_database()
    create_table(conn)
    log_text("get user data")
    sub_hrefs, user_data = spider_user("65b742a2000000000d03d4c5", conn)
    dic = {}
    for index, href in enumerate(sub_hrefs, start=1):
        try:
            get_post(index, href, dic)
        except Exception as e:
            log_text(e)
            continue

    # save key_words
    msg = ""
    for key in dic:
        msg += key + ": " + str(dic[key]) + "; "
    # conn, username, xhs_id, ip, intro, key_words
    insert_data(conn, user_data[0], user_data[1], user_data[2], user_data[3], msg) # ! init a user

    log_text("spider finished tags: ")
    print(dic)
    file.close()
    conn.close()


if __name__ == "__main__":
    main()


driver.quit()

"""
写到数据库里
id(自增) username xhs_id intro ip key_words

"""