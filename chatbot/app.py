
import streamlit as st 
import streamlit.components.v1 as stc
import joblib
import os
import numpy as np
import pandas as pd
import re
import ast

html_temp = """
		<div padding:10px;border-radius:10px">
		<img src="https://imgur.com/ma0W5jF.jpg" style="width: 500px;padding-left: 60px;">
		<h4 style="color:black;text-align:center;">by TMR MDS 8.0 Group A </h4>
		</div>
		"""

def main():
	# st.title("ML Web App with Streamlit")
	stc.html(html_temp)
	st.markdown("""
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
	""", unsafe_allow_html=True)

	# read data
	df = pd.read_csv("./project/course_total.csv")
	# st.dataframe(df)
	df['總影片時長'] = df.總影片時長.str.extract('(\d+)') #只提取數字

	if 'page' not in st.session_state: st.session_state.page = 0 #https://docs.streamlit.io/library/api-reference/session-state
	def nextPage(): st.session_state.page += 1
	def firstPage(): st.session_state.page = 0

	# 宣告變數為全域變數
	global skill, level, hw,speed,interaction, price, result, Ttime, others
	skill = ''
	level = ''
	hw = ''
	star = ''
	speed = ''
	interaction = ''
	price = ''
	result = ''
	Ttime = ''
	others = ''

	## Page 0
	if st.session_state.page == 0:  #第1頁
		needs = st.multiselect('請勾選您在意的課程面向',['教材','講師','價格','時間'])
		course = st.text_input("請輸入您想學的課程")
		if course is not "" and '教材' in needs:
			st.subheader("教材")
			skill = st.select_slider("".join(["您對",course,"的掌握度"]),["完全不熟悉","稍微不熟悉","普通","稍微熟悉","完全熟悉"])
			level = st.select_slider("".join(["您期望的難易度"]),["非常簡單","稍微簡單","普通","稍微困難","非常困難"])
			hw = st.selectbox('您是否希望有作業',("是","否"))
			st.markdown("---")

		if course is not "" and '講師' in needs:
			st.subheader("講師")
			star = st.select_slider("".join(["您期待的評價"]),["1顆星","2顆星","3顆星","4顆星","5顆星"])
			speed = st.select_slider("您期望的語速",["慢","中","快"])
			interaction = st.selectbox('您是否希望老師踴躍回應提問',("是","否"))
			st.markdown("---")

		if course is not "" and '價格' in needs:
			st.subheader("價格")
			price = st.slider("您的預算(元)",0,10000,(1000,3000))
			st.markdown("---")

		if course is not "" and '時間' in needs:
			st.subheader("時間")
			#time = st.slider("您預期的課程*每單元時長*(分鐘)",1,300,(5,60))
			Ttime = st.slider("您預期的課程*總時長*(分鐘)",0,6000,(100,500))
			st.markdown("---")
		if course is not "" and needs is not "":
			others = st.text_input("若有其他需求，請輸入")
		
		# 把使用者輸入的條件儲存起來
		result = {'skill':skill,
		'level':level,
		'hw':hw,
		'star':star,
		'speed':speed,
		'interaction':interaction,
		'price':price,
		'Ttime':Ttime,
		'others':others
		}
		st.session_state.result = result #把result存在session state裡面
		#st.write(st.session_state.result)
		st.button("提交",on_click=nextPage) #點擊提交之後會執行nextpage的function

	## Page 1
	elif st.session_state.page == 1:
		#st.write(st.session_state.result)
		df2 = df
		df2.評價星等 = df2.評價星等.str.extract('(\d+)')
		df2.總影片時長 = df2.總影片時長.str.extract('(\d+)')
		df3 = df2
		dele = []
		for i in range(0,len(df2.index)):
			if (int(df2.總影片時長[i])) not in range(st.session_state.result['Ttime'][0],st.session_state.result['Ttime'][1]): #提取時間
				dele.append(i)
		df3 = df2.drop(dele)

		advices = st.selectbox ("推薦的課程",(df3['課程名稱'].to_numpy())) #讀進df當中的課程名稱當作選項
		for i in range(0,len(df3.index)):
			if advices == df3['課程名稱'][i]:
				st.write(df3["評價標題的結論"][i])
				msg = ast.literal_eval(df3["評價標題的結論"][i])
				st.write(msg)



if __name__ == '__main__':
	main()