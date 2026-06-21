import pandas as pd
import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# =========================
# 读取评论
# =========================
df = pd.read_csv("cleanData.csv")

comments = df["内容"].astype(str)

text = " ".join(comments)

# =========================
# 加载停用词
# =========================
with open("stopwords.txt", "r", encoding="utf-8") as f:
    stopwords = set(
        line.strip()
        for line in f
    )

# =========================
# 分词过滤
# =========================
word_list = []

for word in jieba.cut(text):

    word = word.strip()

    if len(word) < 2:
        continue

    if word in stopwords:
        continue

    word_list.append(word)

result = " ".join(word_list)

# =========================
# 生成词云
# =========================
wc = WordCloud(
    font_path="C:/Windows/Fonts/msyh.ttc",
    width=1920,
    height=1080,
    background_color="white",
    max_words=500
)

wc.generate(result)

wc.to_file("山白非遗词云图.png")

plt.figure(figsize=(12, 8))
plt.imshow(wc)
plt.axis("off")
plt.show()

print("词云图生成成功")