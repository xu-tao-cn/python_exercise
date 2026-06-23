import pandas as pd
import jieba
from collections import Counter
from snownlp import SnowNLP
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

# ==========================
# 字体设置
# ==========================
FONT_PATH = "C:/Windows/Fonts/msyh.ttc"

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei"]
plt.rcParams["axes.unicode_minus"] = False

# ==========================
# 读取数据
# ==========================
df = pd.read_csv("cleanData.csv")

comments = df["内容"].astype(str)

# ==========================
# 读取情感词典
# ==========================
with open("positive.txt", "r", encoding="utf-8") as f:
    positive_dict = set(
        line.strip()
        for line in f
        if line.strip()
    )

with open("negative.txt", "r", encoding="utf-8") as f:
    negative_dict = set(
        line.strip()
        for line in f
        if line.strip()
    )

# ==========================
# 情感统计
# ==========================
positive_words = []
negative_words = []

positive_num = 0
neutral_num = 0
negative_num = 0

scores = []

for comment in comments:

    try:

        score = SnowNLP(comment).sentiments

        scores.append(score)

        if score > 0.6:
            positive_num += 1

        elif score < 0.4:
            negative_num += 1

        else:
            neutral_num += 1

        words = jieba.lcut(comment)

        for word in words:

            if word in positive_dict:
                positive_words.append(word)

            elif word in negative_dict:
                negative_words.append(word)

    except:
        continue

# ==========================
# 词频统计
# ==========================
positive_freq = Counter(positive_words)
negative_freq = Counter(negative_words)

# 防止词云为空
if len(positive_freq) == 0:
    positive_freq = {"积极": 1}

if len(negative_freq) == 0:
    negative_freq = {"消极": 1}

positive_top10 = positive_freq.most_common(10)
negative_top10 = negative_freq.most_common(10)

# ==========================
# 生成词云
# ==========================
wc_positive = WordCloud(
    font_path=FONT_PATH,
    width=1200,
    height=800,
    background_color="white",
    colormap="Reds"
).generate_from_frequencies(positive_freq)

wc_negative = WordCloud(
    font_path=FONT_PATH,
    width=1200,
    height=800,
    background_color="white",
    colormap="Blues"
).generate_from_frequencies(negative_freq)

# ==========================
# 创建画布
# ==========================
fig = plt.figure(figsize=(18, 12))

gs = GridSpec(
    2,
    2,
    figure=fig,
    height_ratios=[1, 1.5]
)

# ==========================
# 左上：情感占比
# ==========================
ax1 = fig.add_subplot(gs[0, 0])

sizes = [
    positive_num,
    neutral_num,
    negative_num
]

labels = [
    "积极",
    "中性",
    "消极"
]

colors = [
    "#e6b8b7",
    "#c0504d",
    "#f79646"
]

ax1.pie(
    sizes,
    labels=labels,
    autopct="%1.1f%%",
    colors=colors,
    startangle=90
)

ax1.set_title(
    "♦ 情感占比",
    fontsize=18,
    color="#7f0000",
    fontweight="bold"
)

# ==========================
# 右上：情感值分布
# ==========================
ax2 = fig.add_subplot(gs[0, 1])

scores_transform = [
    (s * 2) - 1
    for s in scores
]

bins = [
    -1, -0.8, -0.6, -0.4, -0.2,
     0, 0.2, 0.4, 0.6, 0.8, 1
]

intervals = pd.cut(
    scores_transform,
    bins=bins
)

count = pd.Series(
    intervals
).value_counts()

count = count.sort_index()

bar_colors = []

for i in range(len(count)):

    if i < 5:
        bar_colors.append("#1f4e79")

    elif i == 5:
        bar_colors.append("#d9d9d9")

    else:
        bar_colors.append("#b22222")

bars = ax2.bar(
    range(len(count)),
    count.values,
    color=bar_colors
)

for bar in bars:

    h = bar.get_height()

    ax2.text(
        bar.get_x() + bar.get_width() / 2,
        h,
        str(int(h)),
        ha="center",
        fontsize=9
    )

ax2.set_xticks(range(len(count)))

ax2.set_xticklabels(
    [str(i) for i in count.index],
    rotation=25
)

ax2.set_ylabel("评论数量")

ax2.set_title(
    "♦ 情感值与数量分布情况",
    fontsize=18,
    color="#7f0000",
    fontweight="bold"
)

# ==========================
# 左下：积极词云+表格
# ==========================
sub1 = gs[1, 0].subgridspec(
    1,
    2,
    width_ratios=[4, 1]
)

ax3 = fig.add_subplot(sub1[0])

ax3.imshow(wc_positive)

ax3.axis("off")

ax3.set_title(
    "♦ 积极情感词表",
    fontsize=18,
    color="#7f0000",
    fontweight="bold"
)

ax4 = fig.add_subplot(sub1[1])

ax4.axis("off")

table1 = ax4.table(
    cellText=positive_top10,
    colLabels=["关键词", "频次"],
    loc="center"
)

table1.auto_set_font_size(False)
table1.set_fontsize(10)
table1.scale(1.2, 2)

# 表格颜色
for (row, col), cell in table1.get_celld().items():

    if row == 0:
        cell.set_facecolor("#f4cccc")
        cell.set_text_props(weight='bold')
    else:
        cell.set_facecolor("#fde9d9")

# ==========================
# 右下：消极词云+表格
# ==========================
sub2 = gs[1, 1].subgridspec(
    1,
    2,
    width_ratios=[4, 1]
)

ax5 = fig.add_subplot(sub2[0])

ax5.imshow(wc_negative)

ax5.axis("off")

ax5.set_title(
    "♦ 消极情感词表",
    fontsize=18,
    color="#7f0000",
    fontweight="bold"
)

ax6 = fig.add_subplot(sub2[1])

ax6.axis("off")

table2 = ax6.table(
    cellText=negative_top10,
    colLabels=["关键词", "频次"],
    loc="center"
)

table2.auto_set_font_size(False)
table2.set_fontsize(10)
table2.scale(1.2, 2)

for (row, col), cell in table2.get_celld().items():

    if row == 0:
        cell.set_facecolor("#cfe2f3")
        cell.set_text_props(weight='bold')
    else:
        cell.set_facecolor("#eaf3fb")

# ==========================
# 总标题
# ==========================
plt.suptitle(
    "抖音评论情感分析",
    fontsize=28,
    color="#7f0000",
    fontweight="bold"
)

plt.tight_layout()

plt.savefig(
    "情感分析总图.png",
    dpi=600,
    bbox_inches="tight"
)

plt.show()