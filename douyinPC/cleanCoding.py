import pandas as pd
import re
import emoji
from opencc import OpenCC

# ==========================
# 文件路径
# ==========================
INPUT_FILE = "./allData.csv"
OUTPUT_FILE = "./cleanData.csv"

# ==========================
# 读取数据
# ==========================
df = pd.read_csv(INPUT_FILE)

print("原始数据量：", len(df))

# 评论列
COMMENT_COL = "内容"

# ==========================
# 简繁转换
# ==========================
cc = OpenCC('t2s')

# ==========================
# 无意义评论
# ==========================
invalid_words = {
    "666",
    "6666",
    "66666",
    "哈哈",
    "哈哈哈",
    "哈哈哈哈",
    "呵呵",
    "好",
    "好看",
    "不错",
    "支持",
    "牛",
    "牛逼",
    "厉害",
    "棒",
    "赞",
    "顶",
    "打卡",
    "来了",
    "看看",
    "路过",
    "收藏",
    "学习",
    "已阅"
}

# ==========================
# 广告关键词
# ==========================
ad_keywords = [
    "加微信",
    "微信",
    "vx",
    "vx:",
    "v:",
    "qq",
    "企鹅",
    "私聊",
    "联系我",
    "赚钱",
    "兼职",
    "代理",
    "推广",
    "培训",
    "课程",
    "引流",
    "互粉",
    "关注我"
]

# ==========================
# 清洗函数
# ==========================
def clean_text(text):

    if pd.isna(text):
        return None

    text = str(text)

    # 去除换行
    text = text.replace("\n", "")
    text = text.replace("\r", "")

    # 简体统一
    text = cc.convert(text)

    # 删除 @用户
    text = re.sub(r'@[\w\u4e00-\u9fa5_-]+', '', text)

    # 删除话题
    text = re.sub(r'#.*?#', '', text)

    # 删除网址
    text = re.sub(r'http[s]?://\S+', '', text)

    # 删除抖音表情 [赞] [鼓掌]
    text = re.sub(r'\[.*?\]', '', text)

    # 删除emoji
    text = emoji.replace_emoji(text, replace='')

    # 删除特殊符号
    text = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9]', '', text)

    # 去首尾空格
    text = text.strip()

    # 空内容
    if len(text) == 0:
        return None

    # 纯数字
    if text.isdigit():
        return None

    # 无意义短评论
    if text in invalid_words:
        return None

    # 长度太短
    if len(text) <= 2:
        return None

    # 广告过滤
    lower_text = text.lower()

    for keyword in ad_keywords:
        if keyword.lower() in lower_text:
            return None

    # 外文过滤
    chinese_count = len(re.findall(r'[\u4e00-\u9fa5]', text))

    if chinese_count == 0:
        return None

    return text


# ==========================
# 执行清洗
# ==========================
df[COMMENT_COL] = df[COMMENT_COL].apply(clean_text)

# 删除空值
df = df.dropna(subset=[COMMENT_COL])

print("清洗后数据量：", len(df))

# ==========================
# 去重
# ==========================
before = len(df)

df = df.drop_duplicates(subset=[COMMENT_COL])

after = len(df)

print("去重前：", before)
print("去重后：", after)
print("删除重复：", before - after)

# ==========================
# 重置索引
# ==========================
df = df.reset_index(drop=True)

# ==========================
# 保存文件
# ==========================
df.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8-sig"
)

print("================================")
print("数据清洗完成")
print("保存文件：", OUTPUT_FILE)
print("最终数据量：", len(df))
print("================================")