# Initialize by 紫婕
# Modified by Yi-Hsiu (YHL) on 2023/03/27
import pandas as pd
import ast
import openai
import os

# 我有重新命名 csv 檔名稱，所以爬蟲儲存檔案時的名稱可能要再修改!

"""把各個課程的評論整合到course_total"""

# 建立所有課程檔案名稱 list，以存取已爬課程
course_name_list = []
for i in range(10):
    course_name_list.append("course" + str(i + 1) + ".csv")

if os.path.exists('./temp') != True: 
    !mkdir temp

path_list = []
for i in range(10):
    path_list.append(
        os.path.join('./temp', course_name_list[i])
        # "./temp/" + course_name_list[i] + ".csv"
    )

course_total = pd.read_csv(
    "./temp/course_total.csv"
)
list_of_dict = []

for i in range(10):
    course_comment = pd.read_csv(path_list[i])

    dict = {}
    dict["評論標題"] = []
    dict["評論內容"] = []

    for i in range(len(course_comment)):
        dict["評論標題"].append(course_comment["評論標題"][i])
        dict["評論內容"].append(course_comment["評論內容"][i])

    list_of_dict.append(dict)

course_total.insert(7, column="評價標題與內容", value=list_of_dict)

course_total.to_csv("./course_total.csv")

"""串 chatgpt
目前只有針對 "評論標題" 進行分析，
要再針對 "評論內容" 進行分析
prompt 以後可以再修改優化"""

# API key
# openai.api_key = "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" # 紫婕's api key
openai.api_key = "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" # YHL's api key

# 重新讀入 csv
course_total_api = pd.read_csv(
    "./course_total.csv"
)
del course_total_api["Unnamed: 0.1"]
del course_total_api["Unnamed: 0"]

comment_title_summary_total = []
comment_content_summary_total = []

# 針對評論標題
for i in range(len(course_total_api)):
    try:
        msg = ast.literal_eval(course_total_api["評價標題與內容"][i])["評論標題"]
    except:
        msg = "無相關評價"  # 可以試著丟給 chatgpt 的額外資訊: 若無相關評價，請呈現"無相關評價"即可

    # 請 chatgpt 統整評價重點
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        max_tokens=128,
        temperature=0.5,
        messages=[
            {
                "role": "user",
                "content": "下列清單當中，每一項元素為一個課程評價，請將下列的課程評論內容，統整成3個重點，且須最真實反映課程評價: ",
            },
            {"role": "user", "content": str(msg)},
        ],
    )

    comment_title_summary = response.choices[0].message.content
    comment_title_summary = comment_title_summary.split("\n")

    for i in range(len(comment_title_summary)):
        comment_title_summary[i] = comment_title_summary[i][3:]

    comment_title_summary_total.append(comment_title_summary)

type(comment_title_summary_total)
course_total_api.insert(
    len(course_total_api.columns), column="評價標題的結論", value=comment_title_summary_total
)

# 針對評論內容
# 下列 (85 ~ 110列) 的程式碼先不要跑，因為我們給的 tokens 數量太多
# 最多 4097 tokens，我們有 9705 tokens

for i in range(len(course_total_api)):
    try:
        msg = ast.literal_eval(course_total_api["評價標題與內容"][i])["評論內容"]
    except:
        msg = "無相關評價"  # 可以試著丟給 chatgpt 的額外資訊: 若無相關評價，請呈現"無相關評價"即可

    # 請 chatgpt 統整評價重點
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        max_tokens=128,
        temperature=0.5,
        messages=[
            {
                "role": "user",
                "content": "下列清單當中，每一項元素為一個課程評價，請將下列的課程評論內容，統整成3個重點，且須最真實反映課程評價: ",
            },
            {"role": "user", "content": str(msg)},
        ],
    )

    comment_content_summary = response.choices[0].message.content
    comment_content_summary = comment_content_summary.split("\n")

    for i in range(len(comment_content_summary)):
        comment_content_summary[i] = comment_content_summary[i][3:]

    comment_content_summary_total.append(comment_content_summary)

type(comment_content_summary_total)
course_total_api.insert(
    len(course_total_api.columns), column="評價內容的結論", value=comment_content_summary_total
)

# 下面這個要跑，才會更新 csv 檔
course_total_api.to_csv(
    "C:\\Users\\Jye-li\\OneDrive\\桌面\\Course_info\\course_total.csv"
)
