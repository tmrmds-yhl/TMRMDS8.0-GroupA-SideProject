# REVIEW: 建議將使用者輸入的 content 與其他程式分開來，一樣建議要 validate 再後續執行
import streamlit as st 
import streamlit.components.v1 as stc
# import joblib
import os
import numpy as np
import pandas as pd
import re
import ast

import jieba.analyse
import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import jieba.posseg as pseg
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
plt.rcParams['axes.unicode_minus'] = False


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
	#df = pd.read_csv("./project/course_total.csv")
	df = pd.read_csv("./chatbot/Hahow機器學習課程.csv")

	# 把 df 裡面的文字刪掉，只保留數字
	#df['評價星等'] = df['評價星等'].replace(' Stars', '', regex=True).astype(float)
	#df.總影片時長 = df.總影片時長.str.extract('(\d+)').astype(float)
	#df.評論數 = df.評論數.str.extract('(\d+)').astype(float)
	#df.觀看數 = df.觀看數.str.extract('(\d+)').astype(float)
	# 把 df 裡面價格的 "NT$"及","皆取代為空白
	#df['價格'] = df['價格'].replace('NT|[\$,]', '', regex=True).astype(float)

	if 'page' not in st.session_state: st.session_state.page = 0 #https://docs.streamlit.io/library/api-reference/session-state
	def nextPage(): st.session_state.page += 1
	def firstPage(): st.session_state.page = 0

	# 宣告變數為全域變數
	global skill, level, hw,speed,interaction, price, result, Ttime, others, comment, student_num
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
	comment = ''
	student_num = ''

	## Page 0
	if st.session_state.page == 0:  #第1頁
		needs = st.multiselect('請勾選您在意的課程面向',['教材','講師','價格','時間'])
		course = st.selectbox('您想學的課程',['音樂','語言','攝影','藝術','設計','人文','行銷','程式','投資理財','職場技能','手作','生活品味'])
		st.session_state.needs = needs
		st.session_state.course = course
		if course is not "":
			st.button("提交",on_click=nextPage) #點擊提交之後會執行nextpage的function
	
	if st.session_state.page == 1:  #第2頁
		if st.session_state.course is not "" and '教材' in st.session_state.needs:
			st.subheader("教材")
			skill = st.select_slider("".join(["您對",st.session_state.course,"的掌握度"]),["完全不熟悉","稍微不熟悉","普通","稍微熟悉","完全熟悉"])
			level = st.select_slider("".join(["您期望的難易度"]),["非常簡單","稍微簡單","普通","稍微困難","非常困難"])
			hw = st.selectbox('您是否希望有作業',("是","否"))
			comment = st.slider("您期望該課程的評論數量", 0, 500, (0, 100))
			# 把人數的上界調為df裡面人數的最大值，預設選的上下界為最大人數的0.6-0.8，四捨五入到十位數
			student_num = st.slider("您期望該課程的已報名人數", 0, int(df['觀看數'].max()),(int(round(df['觀看數'].max()*0.6,-1)),int(round(df['觀看數'].max()*0.8,-1))))
			st.markdown("---")

		if st.session_state.course is not "" and '講師' in st.session_state.needs:
			st.subheader("講師")
			star = st.slider("您期待的評價(星等)",1, 5, (4, 5))
			speed = st.select_slider("您期望的語速",["慢","中","快"])
			interaction = st.selectbox('您是否希望老師踴躍回應提問',("是","否"))
			st.markdown("---")

		if st.session_state.course is not "" and '價格' in st.session_state.needs:
			st.subheader("價格")
			# 把價格的上界調為df裡面價格的最大值，預設選的上下界為最大價格的0.6-0.8，四捨五入到百位數
			price = st.slider("您的預算(元)",0,int(df['價格'].max()),(int(round(df['價格'].max()*0.6,-2)),int(round(df['價格'].max()*0.8,-2))))
			st.markdown("---")

		if st.session_state.course is not "" and '時間' in st.session_state.needs:
			st.subheader("時間")
			#time = st.slider("您預期的課程*每單元時長*(分鐘)",1,300,(5,60))
			# 把時長的上界調為df裡面時長的最大值，預設選的上下界為最大時長的0.6-0.8，四捨五入到百位數
			Ttime = st.slider("您預期的課程*總時長*(分鐘)",0,int(df['總影片時長'].max()),(int(round(df['總影片時長'].max()*0.6,-2)),int(round(df['總影片時長'].max()*0.8,-2))))
			st.markdown("---")
		if st.session_state.course is not "" and st.session_state.needs is not "":
			others = st.text_input("若有其他需求，請輸入")

		# 把使用者輸入的條件儲存起來
		# 建議用 class 儲存而非 dictionary
		result = {'skill':skill,
		'level':level,
		'hw':hw,
		'star':star,
		'speed':speed,
		'interaction':interaction,
		'price':price,
		'Ttime':Ttime,
		'others':others,
		"comment": comment,
		"student_num": student_num
		}
		st.session_state.result = result #把result存在session state裡面
		#st.write(st.session_state.result)
		st.button("開始篩選",on_click=nextPage) #點擊提交之後會執行nextpage的function

	## Page 1
	elif st.session_state.page == 2:
		#st.write(st.session_state.result)

		# 命名不要偷懶喔 XD，如果是要複製請標注 copy 不然有可能會連同 df 一起修改到
		df2 = df.copy()

		# 初步篩選
		df3 = df2
		dele = []
		st.dataframe(df3) # 學長自己查看用的

		# 篩選直接用 pandas 的 method 即可，舉例:
		########
		def user_filter(df):
			if st.session_state.result['Ttime']:
				st.dataframe(
					df2
					.loc[lambda temp_df: temp_df['總影片時長'].between(
						st.session_state.result['Ttime'][0], st.session_state.result['Ttime'][1]
					)]
				)
			
		st.write(st.session_state.result['Ttime'])
		st.dataframe(
			df2
			.pipe(user_filter)
		)
		#########

		# 篩影片時長
		for i in range(0, len(df2.index)):
			try:
				if (int(df2.總影片時長[i])) not in range(st.session_state.result['Ttime'][0],st.session_state.result['Ttime'][1]):
					dele.append(i)
			except:
				pass

		# 篩評價星等
		for i in range(0, len(df2.index)):
			try: 
				if (int(df2.評價星等[i])) not in range(st.session_state.result['star'][0],st.session_state.result['star'][1]):
					dele.append(i)
			except:
				pass
		
		# 篩評論數
		for i in range(0, len(df2.index)):
			try: 
				if (int(df2.評論數[i])) not in range(st.session_state.result['comment'][0],st.session_state.result['comment'][1]):
					dele.append(i)
			except:
				pass
		
		# 篩觀看數
		for i in range(0, len(df2.index)):
			try: 
				if (int(df2.觀看數[i])) not in range(st.session_state.result['student_num'][0],st.session_state.result['student_num'][1]):
					dele.append(i)
			except:
				pass
		
		# 篩價格
		for i in range(0, len(df2.index)):
		 	try: 
		 		if (int(df2.價格[i])) not in range(st.session_state.result['price'][0],st.session_state.result['price'][1]):
		 			dele.append(i)
		 	except:
		 		pass



		# 刪除 dele 裡面的重複值
		dele = list(set(dele))


		# 刪除不符合條件的課程(列)
		df3 = df2.drop(dele)

		# 篩選後超過十個按照評價星等選出前十
		if len(df3.index) > 10:
			df3.sort_values(by='評價星等', ascending=False)
			df3 = df3.head(10)

		advices = st.selectbox ("推薦的課程",(df3['課程名稱'].to_numpy())) #讀進df當中的課程名稱當作選項
		
		# 重置 df3 的 index，並刪除用不到的欄位
		df3 = df3.reset_index()
		del df3["index"]
		del df3["Unnamed: 0"]

		for i in range(0,len(df3.index)):
			# st.write(df3)
			# st.write(df3["課程名稱"].to_numpy())

			if advices == df3['課程名稱'][i]:

					#st.write(df3["評價標題"])
					msg = ast.literal_eval(df3["評論內容"][i])

					jieba.set_dictionary('./chatbot/dict.txt.big')
					text = ("".join(msg))
					cut_text = " ".join(jieba.cut(text))
					# 因為有很多贅詞，所以只留下形容詞
					words =pseg.cut(cut_text)
					adj = ['Ag','a','ad','an']
					adjwords = []
					for w in words:
						if(w.flag in adj): #w.flag:看詞性
							adjwords.append(w.word)
					adjwords = (" ".join(adjwords)) #轉string

					# 畫出文字雲
					wordcloud = WordCloud(collocations=False,
                      font_path='./chatbot/msj.ttf',
                      width=800,
                      height=600,
                      margin=2).generate(adjwords)
					
					st.image(wordcloud.to_image())
			
			# 有些沒有原始評價的課程，其課程評價結論的 list 只會有一個元素 (-> "我無法回答這個問題...")
			# 之後如果要把評價結論一列一列呈現的話要注意! (也許可用 try except 功能)

		# 點擊重新篩選會執行firstPage，回到第1頁輸入課程的部分
		st.button("重新篩選",on_click=firstPage)


if __name__ == '__main__':
	main()