# TMRMDS8.0-GroupA-SideProject

!! Demo 用 "機器學習課程_first_10.csv" !!
如果bug很多的話可以先用 "course_total.csv"

# Quickstart
Create a virutual environment using venv:
```
py -3.10 -m venv .venv
```
Activate the new environment by finding the `Scripts` (Windows) or `bin` (Mac).

Windows: drag and drop the `Activate.ps1` into the powershell terminal
Mac: Type: `source` and then drag and drop `activate` file into the zsh terminal

Install from requirements.txt
```
pip install -r requirements.txt
```

# Review Notes
- venv 虛擬環境建置
- 將 source code 放到 src folder 中，再去整理，若爬蟲 code 已經完成，可以將齊放到另一個資料夾表示做為爬蟲 final code
- 記得像是 api key 都不要上傳給別人看，可以將 api key 存進一個檔案中 (ie. json file)，然後將這個 json 檔放到 .gitignore 裡
- checkout get_coursedata.py 來看一下如何 parse request.get 下來的資料並存成 dataframe
- reviews:
	- /chatbot/app.py
	- /src/api爬蟲.py
	- /src/建置資料庫.py
	- README.md
	- requirements.txt