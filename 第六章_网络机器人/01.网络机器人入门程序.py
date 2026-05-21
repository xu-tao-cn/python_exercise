import requests
from lxml import html

# 定义url
url = "https://www.tiobe.com"

# 发送请求，获取数据
data = requests.get(url)

# 输出数据到控制台
print(data.text)
