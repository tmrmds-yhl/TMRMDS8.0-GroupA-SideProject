import time
import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
from bs4 import BeautifulSoup as Soup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

# Hello
search = "機器學習"


def move_file(dectect_name, folder_name):
    """
    dectect_name:
    folder_name:
    """
    import os

    save = []
    for i in os.listdir():
        if dectect_name in i:
            save.append(i)

    ff = [i for i in save if not "." in i]
    ff = [i for i in ff if "（" in i]

    try:
        os.makedirs(folder_name)
        folder_namenew = folder_name

    except:
        try:
            os.makedirs(folder_name + "（" + str(0) + "）")
            folder_namenew = folder_name + "（" + str(0) + "）"
        except:
            for i in range(0, 10):
                iinn = [j for j in ff if folder_name + "（" + str(i) + "）" in j]
                if len(iinn) == 0:
                    os.makedirs(folder_name + "（" + str(i) + "）")
                    folder_namenew = folder_name + "（" + str(i) + "）"
                    break

    import shutil

    save = [i for i in save if "." in i]
    for m in save:
        shutil.move(m, folder_namenew)


def collect_comments(browser, number, coursename):
    # 點選第一堂課
    WebDriverWait(browser, 30).until(
        EC.presence_of_element_located((By.CLASS_NAME, "title.marg-t-20.marg-b-10"))
    )
    # search_click = browser.find_elements_by_class_name('title.marg-t-20.marg-b-10')[0]
    search_click = browser.find_elements_by_class_name("title.marg-t-20.marg-b-10")[
        number
    ]
    search_click.click()

    # 點選所有評論
    WebDriverWait(browser, 30).until(
        EC.presence_of_element_located((By.CLASS_NAME, "sc-hvnn7l-2.bcCbbE"))
    )
    search_click = browser.find_elements_by_class_name("sc-hvnn7l-2.bcCbbE")[1]
    search_click.click()

    # 點看更多
    while True:
        try:
            WebDriverWait(browser, 30).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, "sc-1a6j6ze-0.cYdxxq.sc-b21euj-2.buAXqm")
                )
            )
            search_click = browser.find_element_by_class_name(
                "sc-1a6j6ze-0.cYdxxq.sc-b21euj-2.buAXqm"
            )
            search_click.click()
        except:
            break

    # 爬取主評論、副評論
    main_comment = []
    sub_comment = []
    soup = Soup(browser.page_source, "lxml")

    count = len(soup.find_all("p", {"class": "text-strong marg-b-5"}))
    if count != 0:
        for i in range(count):
            catch = soup.find_all("p", {"class": "text-strong marg-b-5"})[i].text
            main_comment.append(catch)
        for i in range(count):
            catch = soup.find_all("p", {"class": "sc-wei2cc-0 idlgCC"})[i].text
            sub_comment.append(catch)
    else:
        main_comment.append("N/A")
        sub_comment.append("N/A")

    comments = pd.DataFrame(
        {
            "評論標題": main_comment,
            "評論內容": sub_comment,
        }
    )

    comments.to_csv(f"Hahow{search}：課程{number+1} 課程評論.csv", encoding="UTF-8-sig")

    browser.back()
    browser.back()
    time.sleep(2)


def course_searching(search):
    url = "https://hahow.in/"
    browser.get(url)

    time.sleep(8)

    # 輸入關鍵字
    WebDriverWait(browser, 30).until(
        EC.presence_of_element_located((By.CLASS_NAME, "sc-3izbpp-3.fVBoBi"))
    )
    search_input = browser.find_elements_by_class_name("sc-3izbpp-3.fVBoBi")[0]
    search_input.send_keys(search)

    # 點選搜尋鍵
    WebDriverWait(browser, 30).until(
        EC.presence_of_element_located((By.CLASS_NAME, "sc-3izbpp-0.cwlbXJ"))
    )
    search_click = browser.find_elements_by_class_name("sc-3izbpp-0.cwlbXJ")[0]
    search_click.click()

    # 點選影音課程
    WebDriverWait(browser, 30).until(
        EC.presence_of_element_located((By.CLASS_NAME, "sc-v1wcho-1.bqEVBe"))
    )
    search_click = browser.find_elements_by_class_name("sc-v1wcho-1.bqEVBe")[1]
    search_click.click()
    time.sleep(1.5)

    soup = Soup(browser.page_source, "lxml")
    course_name = []
    ratings = []
    commenters = []
    video_length = []
    viewers = []
    pricings = []

    # 爬取課程名稱
    try:
        for i in range(10):
            catch = soup.find_all("h4", {"class": "title marg-t-20 marg-b-10"})[i].text
            course_name.append(catch)
    except:
        course_name.append("-")
        pass

    # 爬取評價星等
    try:
        for i in range(10):
            catch = soup.find_all("div", {"class": "star-ratings"})[i].get("title")
            ratings.append(catch)
    except:
        ratings.append("-")
        pass

    # 爬取評論數
    try:
        for i in range(10):
            catch = soup.find_all("div", {"class": "rating"})[i].text
            commenters.append(catch)
    except:
        commenters.append("-")
        pass

    # 爬取總時長
    try:
        for i in range(0, 19, 2):
            catch = soup.find_all("div", {"class": "pull-left"})[i].text
            video_length.append(catch)
    except:
        video_length.append("-")
        pass

    # 爬取總學生數
    try:
        for i in range(1, 20, 2):
            catch = soup.find_all("div", {"class": "pull-left"})[i].text
            viewers.append(catch)
    except:
        viewers.append("-")
        pass

    # 爬取價格
    try:
        for i in range(10):
            catch = soup.find_all("div", {"class": "pull-right"})[i].text
            pricings.append(catch)
    except:
        pricings.append("-")
        pass

    course = pd.DataFrame(
        {
            "課程名稱": course_name,
            "評價星等": ratings,
            "評論數": commenters,
            "總影片時長": video_length,
            "觀看數": viewers,
            "價格": pricings,
        }
    )

    course.to_csv(f"Hahow{search}十大課程.csv", encoding="UTF-8-sig")

    time.sleep(5)

    for i in range(10):
        collect_comments(browser, i, course_name[i])

    move_file(dectect_name=search, folder_name=f"{search}課程資料")

    browser.close()


if __name__ == "__main__":
    course_searching(search)
