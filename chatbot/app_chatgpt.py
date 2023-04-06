import streamlit as st
import streamlit.components.v1 as stc
import joblib
import os
import numpy as np
import pandas as pd
import re
import ast
import openai
from st_aggrid import (
    AgGrid,
    DataReturnMode,
    GridUpdateMode,
    GridOptionsBuilder,
    ColumnsAutoSizeMode,
)


html_temp = """
		<div padding:10px;border-radius:10px">
		<img src="https://imgur.com/ma0W5jF.jpg" style="width: 500px;padding-left: 60px;">
		<h4 style="color:black;text-align:center;">by TMR MDS 8.0 Group A </h4>
		</div>
		"""


def main():
    # st.title("ML Web App with Streamlit")
    stc.html(html_temp)
    st.markdown(
        """
	<style>
	.css-184tjsw p {
    word-break: break-word;
    font-size: 18px;
    font-weight: 600;
	padding-bottom: 10px;
    padding-top: 10px;
	}
	.st-el {
    background-color: rgb(109 194 231);
	}
	</style>
	""",
        unsafe_allow_html=True,
    )

    if "page" not in st.session_state:
        st.session_state.page = (
            0  # https://docs.streamlit.io/library/api-reference/session-state
        )

    def nextPage():
        st.session_state.page += 1

    def firstPage():
        st.session_state.page = 0

    # 宣告變數為全域變數
    global skill, level, hw, speed, interaction, price, result, Ttime, others, comment, student_num, course, df
    skill = ""
    level = ""
    hw = ""
    star = ""
    speed = ""
    interaction = ""
    price = ""
    result = ""
    Ttime = ""
    others = ""
    comment = ""
    student_num = ""
    course = ""
    df = ""
    ## Page 0
    if st.session_state.page == 0:  # 第1頁
        needs = st.multiselect("請勾選您在意的課程面向", ["教材", "講師", "價格", "時間"])
        level_two_options = {
            "音樂": ["樂器", "音樂創作", "音樂理論", "人聲", "DJ"],
            "語言": ["英文", "日文", "韓文", "西班牙文", "歐洲語言", "翻譯"],
            "攝影": ["影像創作", "商業攝影", "後製剪輯", "動態攝影", "影視創作", "攝影理論"],
            "藝術": ["電腦繪圖", "角色設計", "手寫字", "繪畫與插畫", "字體設計", "素描", "色彩學", "表演藝術"],
            "設計": ["動態設計", "平面設計", "應用設計", "網頁設計", "介面設計", "設計理論"],
            "人文": ["文學", "社會科學"],
            "行銷": ["文案", "數位行銷", "社群行銷", "數據分析"],
            "程式": [
                "資料科學",
                "區塊鏈",
                "量化分析",
                "程式理財",
                "程式思維",
                "程式入門",
                "網站架設",
                "手機程式開發",
                "網頁前端",
                "網頁後端",
                "資訊安全",
                "程式語言",
                "遊戲開發",
                "軟體程式開發與維護",
                "AI",
                "人工智慧",
            ],
            "投資理財": ["理財", "投資觀念", "金融商品", "量化交易", "更多投資理財", "比特幣"],
            "職場技能": ["資料彙整", "效率提升", "職場溝通", "文書處理", "求職創業", "獨立接案", "產品設計", "個人品牌經營"],
            "手作": ["模型", "刺繡", "篆刻", "氣球", "手工印刷", "手工書", "手作小物"],
            "生活品味": [
                "運動",
                "寵物",
                "烹飪料理與甜點",
                "數學",
                "心靈成長與教育",
                "壓力舒緩",
                "護膚保養與化妝",
                "親子教育",
                "居家",
                "靈性發展",
                "花草園藝",
            ],
        }
        topic = "程式"
        topic = st.selectbox(
            "您想學習的主題",
            [
                "程式",
                "音樂",
                "語言",
                "攝影",
                "藝術",
                "設計",
                "人文",
                "行銷",
                "投資理財",
                "職場技能",
                "手作",
                "生活品味",
            ],
        )
        course = st.selectbox("您想學習的面向", level_two_options[topic])

    # read data
        
        course_name = "./project/TMRMDS8.0-GroupA-SideProject/Hahow全課程/"+course+".csv"
        df = pd.read_csv(
            course_name
            #"/Users/uscer/Desktop/TMR/sideProject/TMRMDS8.0-GroupA-SideProject/temp/course_total.csv"
        )
        st.session_state.needs = needs
        st.session_state.course = course
        if course is not "":
            st.button("提交", on_click=nextPage)  # 點擊提交之後會執行nextpage的function
    if st.session_state.page == 1:  # 第2頁
        if st.session_state.course is not "" and "教材" in st.session_state.needs:
            st.subheader("教材")
            skill = st.select_slider(
                "".join(["您對", st.session_state.course, "的掌握度"]),
                ["完全不熟悉", "稍微不熟悉", "普通", "稍微熟悉", "完全熟悉"],
            )
            level = st.select_slider(
                "".join(["您期望的難易度"]), ["非常簡單", "稍微簡單", "普通", "稍微困難", "非常困難"]
            )
            hw = st.selectbox("您是否希望有作業", ("是", "否"))
            comment = st.slider("您期望該課程的評論數量", 0, 500, (0, 100))
            # 把人數的上界調為df裡面人數的最大值，預設選的上下界為最大人數的0.6-0.8，四捨五入到十位數
            student_num = st.slider(
                "您期望該課程的已報名人數",
                0,
                int(df["觀看數"].max()),
                (
                    int(round(df["觀看數"].max() * 0.6, -1)),
                    int(round(df["觀看數"].max() * 0.8, -1)),
                ),
            )
            st.markdown("---")

        if st.session_state.course is not "" and "講師" in st.session_state.needs:
            st.subheader("講師")
            star = st.slider("您期待的評價(星等)", 1, 5, (4, 5))
            speed = st.select_slider("您期望的語速", ["慢", "中", "快"])
            interaction = st.selectbox("您是否希望老師踴躍回應提問", ("是", "否"))
            st.markdown("---")

        if st.session_state.course is not "" and "價格" in st.session_state.needs:
            st.subheader("價格")
            # 把價格的上界調為df裡面價格的最大值，預設選的上下界為最大價格的0.6-0.8，四捨五入到百位數
            price = st.slider(
                "您的預算(元)",
                0,
                int(df["價格"].max()),
                (
                    int(round(df["價格"].max() * 0.6, -2)),
                    int(round(df["價格"].max() * 0.8, -2)),
                ),
            )
            st.markdown("---")

        if st.session_state.course is not "" and "時間" in st.session_state.needs:
            st.subheader("時間")
            # time = st.slider("您預期的課程*每單元時長*(分鐘)",1,300,(5,60))
            # 把時長的上界調為df裡面時長的最大值，預設選的上下界為最大時長的0.6-0.8，四捨五入到百位數
            Ttime = st.slider(
                "您預期的課程*總時長*(分鐘)",
                0,
                int(df["總影片時長"].max()),
                (
                    int(round(df["總影片時長"].max() * 0.6, -2)),
                    int(round(df["總影片時長"].max() * 0.8, -2)),
                ),
            )
            st.markdown("---")
        if st.session_state.course is not "" and st.session_state.needs is not "":
            others = st.text_input("請輸入其他需求，若無請填寫「無」，並按Enter")

        # 把使用者輸入的條件儲存起來
        result = {
            "skill": skill,
            "level": level,
            "hw": hw,
            "star": star,
            "speed": speed,
            "interaction": interaction,
            "price": price,
            "Ttime": Ttime,
            "others": others,
            "comment": comment,
            "student_num": student_num,
        }
        st.session_state.result = result  # 把result存在session state裡面
        # st.write(st.session_state.result)
        if others is not "":
            st.button("開始篩選", on_click=nextPage)  # 點擊提交之後會執行nextpage的function

    ## Page 1
    elif st.session_state.page == 2:
        # st.write(st.session_state.result)
        df2 = df

        # 初步篩選
        df3 = df2
        dele = []

        # 篩影片時長
        for i in range(0, len(df2.index)):
            try:
                if (int(df2.總影片時長[i])) not in range(
                    st.session_state.result["Ttime"][0],
                    st.session_state.result["Ttime"][1],
                ):
                    dele.append(i)
            except:
                pass

        # 篩評價星等
        for i in range(0, len(df2.index)):
            try:
                if (int(df2.評價星等[i])) not in range(
                    st.session_state.result["star"][0],
                    st.session_state.result["star"][1],
                ):
                    dele.append(i)
            except:
                pass

        # 篩評論數
        for i in range(0, len(df2.index)):
            try:
                if (int(df2.評論數[i])) not in range(
                    st.session_state.result["comment"][0],
                    st.session_state.result["comment"][1],
                ):
                    dele.append(i)
            except:
                pass

        # 篩觀看數
        for i in range(0, len(df2.index)):
            try:
                if (int(df2.觀看數[i])) not in range(
                    st.session_state.result["student_num"][0],
                    st.session_state.result["student_num"][1],
                ):
                    dele.append(i)
            except:
                pass

        # 篩價格
        for i in range(0, len(df2.index)):
            try:
                if (int(df2.價格[i])) not in range(
                    st.session_state.result["price"][0],
                    st.session_state.result["price"][1],
                ):
                    dele.append(i)
            except:
                pass

        # 刪除 dele 裡面的重複值
        dele = list(set(dele))

        # 刪除不符合條件的課程(列)
        df3 = df2.drop(dele)

        # attach ChatGPT
        openai.api_key = "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"  # YHL's api key, should be changed to TMR's
        df3 = df3.reset_index()
        msg = "現在有%d門課程如下：" % (df3.shape[0])
        for iCourse in range(df3.shape[0]):
            msg += str(
                f"""\n\n第{iCourse+1}門評價為{df3['評價星等'][iCourse]}/5，{df3['價格'][iCourse]}元、總時長為{df3['總影片時長'][iCourse]}分鐘，觀看人數為{df3['觀看數'][iCourse]}人，{df3['評價標題的結論'][iCourse].replace('[', '').replace(']', '').replace("'",'').replace("。, ", "，", 2)}"""
            )
        msg += f"""\n\n 現有一位同學想要學習{st.session_state.course}，"""
        if st.session_state.result["skill"] is not "":
            msg += f"""他對這個技能{st.session_state.result["skill"]}，"""
        if st.session_state.result["level"] is not "":
            msg += f"""期待學習{st.session_state.result["level"]}程度的課程，"""
        if st.session_state.result["others"] is not "":
            msg += f"""同時該同學也有要求：「{st.session_state.result["others"]}」，"""
        msg += "請幫他從上述課程中，推薦三門、並按照推薦順序排列，回傳課程序號，並告訴我各自的原因。"
        st.write(msg)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            max_tokens=500,
            temperature=0.5,
            messages=[{"role": "user", "content": msg}],
        )

        comment_content = response.choices[0].message.content
        comment_content = comment_content.split("\n")
        # comment_content = [
        #     "推薦順序：第3門、第1門、第2門。",
        #     "",
        #     "原因：",
        #     "1. 第3門課程評價最高，且學員反應課程內容豐富且實用性高，對工作有很大的幫助，教學內容從理論到實踐都很完整，物超所值。",
        #     "2. 第1門課程評價次高，且適合初學者，能夠讓學員對Azure操作有基礎認識，內容清晰易懂，且完整且詳細，又入門機器學習。",
        #     "3. 第2門課程評價稍低，但仍有不少學員認為是一個很棒的入門課程，內容豐富多元，對初學者來說有些部分可能會覺得深奧，但整體而言是很棒的課程。",
        # ]

        comment_content = list(filter(None, comment_content))  # Trim string list

        # 篩選出符合條件的課程，利用課程的 index
        suggests = [int(s) - 1 for s in re.findall(r"\d+", comment_content[0])]
        df3 = df3.iloc[suggests, :]
        # 重置 df3 的 index，並刪除用不到的欄位
        df3 = df3.reset_index()
        del df3["index"]
        del df3["Unnamed: 0"]

        comment_content[0] = (
            comment_content[0]
            .replace("第{}門".format(suggests[0] + 1), "\n\n" + df3["課程名稱"][0])
            .replace("第{}門".format(suggests[1] + 1), "\n\n" + df3["課程名稱"][1])
            .replace("第{}門".format(suggests[2] + 1), "\n\n" + df3["課程名稱"][2])
        )

        st.success(comment_content[0])  # 推薦順序: ...
        reason = [
            comment_content[-3].replace(
                "第{}門".format(suggests[0] + 1), df3["課程名稱"][0] + "：\n\n"
            ),
            comment_content[-2].replace(
                "第{}門".format(suggests[1] + 1), df3["課程名稱"][1] + "：\n\n"
            ),
            comment_content[-1].replace(
                "第{}門".format(suggests[2] + 1), df3["課程名稱"][2] + "：\n\n"
            ),
        ]

        advices = st.selectbox("推薦的課程", (df3["課程名稱"].to_numpy()))  # 讀進df當中的課程名稱當作選項

        for i in range(0, len(df3.index)):
            # st.write(df3)
            # st.write(df3["課程名稱"].to_numpy())

            if advices == df3["課程名稱"][i]:
                course_comment = []
                st.success(reason[i])  # 呈現推薦原因

                # 根據有無課程評價選擇呈現的內容
                # 有課程評價 len > 1
                if len(df3["評價標題的結論"]) > 1:
                    summary = ast.literal_eval(df3["評價標題的結論"][i])
                    for j in range(3):
                        course_comment.append(summary[j])
                    suggestion_dict = {"課程評價": course_comment}
                    suggestion_df = pd.DataFrame.from_dict(suggestion_dict)

                    options_builder = GridOptionsBuilder.from_dataframe(suggestion_df)
                    options_builder.configure_default_column(
                        groupable=True,
                        value=True,
                        enableRowGroup=True,
                        aggFunc="sum",
                        editable=True,
                        autoHeight=True,
                    )
                    grid_options = options_builder.build()
                    grid_return = AgGrid(
                        suggestion_df,
                        grid_options,
                        columns_auto_size_mode=ColumnsAutoSizeMode.FIT_ALL_COLUMNS_TO_VIEW,
                    )  # , theme="blue"

                    # st.write(df3["評價標題的結論"][i])
                    # msg = ast.literal_eval(df3["評價標題的結論"][i])
                    # st.write(msg)

                # 無課程評價 len == 1
                elif len(df3["評價標題的結論"]) == 1:
                    st.warning("該課程無相關評價")
                    # st.write("該課程無相關評價")

        # 把推薦課程序號、原因、課程評價整理成一個表格呈現
        # course_comment = []
        # for i in suggests:
        #     course_comment.append(df3["評價標題的結論"][i])

        # suggestion_dict = {"課程編號": suggests, "推薦原因": [comment_content[3], comment_content[4], comment_content[5]], "課程評價": course_comment}
        # suggestion_df = pd.DataFrame.from_dict(suggestion_dict)

        # options_builder = GridOptionsBuilder.from_dataframe(suggestion_df)
        # options_builder.configure_default_column(groupable = True, value = True, enableRowGroup = True, aggFunc = "sum", editable = True, autoHeight = True)
        # options_builder.configure_column("課程編號", pinned = "left")
        # grid_options = options_builder.build()
        # grid_return = AgGrid(suggestion_df, grid_options, theme = "blue")

        # 有些沒有原始評價的課程，其課程評價結論的 list 只會有一個元素 (-> "我無法回答這個問題...")
        # 之後如果要把評價結論一列一列呈現的話要注意! (也許可用 try except 功能)

        # 點擊重新篩選會執行firstPage，回到第1頁輸入課程的部分
        st.button("重新篩選", on_click=firstPage)


if __name__ == "__main__":
    main()
