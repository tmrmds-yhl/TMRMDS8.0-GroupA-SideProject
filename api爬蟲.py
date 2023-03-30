import requests
import json
import time
import numpy as np
import os
from bs4 import BeautifulSoup
import pandas as pd
import datetime

search = '數據分析'
# test
def collect_comments(main_comment, sub_comment, id):
    page = 0
    title = []
    description = []
    while True:
        url = f'https://api.hahow.in/api/courses/{id}/feedbacks?limit=30&page={page}'
        #url = f'https://api.hahow.in/api/courses/597df7e2acc137070007013c/feedbacks?limit=30&page={page}'

        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                    'AppleWebKit/537.36 (KHTML, like Gecko) '
                                    'Chrome/59.0.3071.115 Safari/537.36'}
        resp_feedbacks = requests.get(url, headers=headers).json()
        
        if resp_feedbacks == []:
            break

        for i in range(len(resp_feedbacks)):
            if resp_feedbacks[i]['status'] == 'PUBLISHED':
                title.append(resp_feedbacks[i]['title'])
                description.append(resp_feedbacks[i]['description'])
        page+=1

    main_comment.append(title)
    sub_comment.append(description)

def course_searching(search):
    url = f'https://api.hahow.in/api/products/search?limit=100&query={search}&filter=PUBLISHED'

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                'AppleWebKit/537.36 (KHTML, like Gecko) '
                                'Chrome/59.0.3071.115 Safari/537.36'}

    resp_courses = requests.get(url, headers=headers).json()

    courseN = resp_courses["data"]['courseData']['productCount']
    course_id=[]
    course_name=[]
    ratings=[]
    commenters=[]
    video_length=[]
    viewers=[]
    pricings=[]

    for i in range(courseN):
        course_id.append(resp_courses["data"]['courseData']['products'][i]["_id"])
        course_name.append(resp_courses["data"]['courseData']['products'][i]["title"])
        ratings.append(resp_courses["data"]['courseData']['products'][i]["averageRating"])
        commenters.append(resp_courses["data"]['courseData']['products'][i]["numRating"])
        video_length.append(resp_courses["data"]['courseData']['products'][i]["totalVideoLengthInSeconds"])
        viewers.append(resp_courses["data"]['courseData']['products'][i]["numSoldTickets"])
        pricings.append(resp_courses["data"]['courseData']['products'][i]["price"])

    main_comment = []
    sub_comment = []

    for i in range(courseN):
        collect_comments(main_comment, sub_comment, course_id[i])

    course=pd.DataFrame({
        "課程名稱":course_name,
        "評價星等":ratings,
        "評論數":commenters,
        "總影片時長":video_length,
        "觀看數":viewers,
        "價格":pricings,
        "評論標題":main_comment,
        "評論內容":sub_comment})
    course.to_csv(f'Hahow{search}課程.csv', encoding = 'UTF-8-sig')

if __name__ == '__main__':
    course_searching(search)




