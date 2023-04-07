#%%
from pydantic import BaseModel
import requests
import pandas as pd

SEARCH = '後製剪輯'

# 自動 validate 資料，還有更多 customize 的 validate 方式在套件中
class CourseData(BaseModel):
    _id: str
    title: str
    averageRating: float
    numRating: int
    totalVideoLengthInSeconds: int
    numSoldTickets: int
    price: int

url = f'https://api.hahow.in/api/products/search?limit=100&query={SEARCH}&filter=PUBLISHED'

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                            'AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/59.0.3071.115 Safari/537.36'}

resp_courses = requests.get(url, headers=headers).json()
coursedata = resp_courses["data"]['courseData']
data = [CourseData(**i) for i in coursedata['products']]
pd.DataFrame([item.dict() for item in data])

# %%
