import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
import jieba
from collections import Counter
import re
from wordcloud import WordCloud
import numpy as np

# 设置中文字体
rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
rcParams['axes.unicode_minus'] = False

# 读取CSV文件
df = pd.read_csv('comment.csv')

print(f"总评论数: {len(df)}")

# 定义情感分类词典
positive_emotions = {
    # 赞美类
    '厉害': 5, '牛逼': 5, '棒': 4, '好': 3, '赞': 5, '佩服': 5, '敬佩': 5,
    '惊叹': 4, '震撼': 5, '惊艳': 5, '精美': 4, '精致': 4, '精湛': 5,
    '巧夺天工': 5, '叹为观止': 5, '五体投地': 5, '顶级': 4, '完美': 5,
    '优秀': 4, '伟大': 5, '智慧': 4, '聪明': 3, '精巧': 4,
    
    # 喜爱类
    '喜欢': 4, '爱': 4, '享受': 4, '舒服': 3, '治愈': 4, '平静': 3,
    '美好': 4, '美': 3, '好看': 3, '漂亮': 3, '可爱': 3,
    
    # 感谢类
    '感谢': 4, '感恩': 4, '谢谢': 3, '致敬': 5,
    
    # 支持类
    '支持': 4, '传承': 4, '保留': 3, '发扬': 4, '加油': 3,
    
    # 惊讶类
    '震惊': 4, '不可思议': 4, '难以置信': 4, '天呐': 3, '哇': 3,
}

negative_emotions = {
    # 担忧类
    '担心': -3, '可惜': -3, '遗憾': -3, '失传': -4, '消失': -4,
    '退化': -3, '心疼': -3, '流泪': -2, '哭': -2,
    
    # 负面评价
    '贵': -2, '买不起': -2, '穷': -2, '无聊': -2, '浮躁': -2,
}

neutral_keywords = {
    '手工': 2, '手艺': 2, '匠人': 3, '工匠': 3, '非遗': 3, '传统': 2,
    '文化': 2, '老祖宗': 3, '中华文化': 3, '华夏': 2, '奢侈品': 2,
    '松塔': 1, '香薰': 1, '工艺': 2, '制作': 1, '中国': 1,
}

# 提取所有评论内容
all_content = ' '.join(df['内容'].dropna().astype(str))

# 使用jieba分词
words = jieba.lcut(all_content)

# 过滤停用词
stop_words = {
    '的', '了', '是', '在', '我', '有', '和', '就', '不', '人', '都', '一', 
    '一个', '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有',
    '看', '自己', '这', '他', '她', '它', '们', '那', '些', '什么', '怎么',
    '这个', '那个', '这么', '那么', '真的', '可以', '被', '让', '能', '做', '才',
    '还', '已经', '但是', '因为', '所以', '如果', '虽然', '而', '与', '及', '等',
    '我们', '他们', '你们', '这样', '那样', '这里', '那里', '哪里',
    '啊', '呀', '呢', '吧', '嘛', '哦', '嗯', '哈', '啦', '呗',
    '一种', '一下', '一些', '一点', '一直', '一起',
}

# 过滤单字、数字、标点和停用词
filtered_words = [
    word for word in words 
    if len(word) > 1 
    and word not in stop_words 
    and not re.match(r'^[\d\W]+$', word)
]

# 统计词频
word_counter = Counter(filtered_words)

# 创建情感权重字典
emotion_weights = {}
for word, count in word_counter.items():
    weight = 0
    
    # 检查是否在情感词典中
    if word in positive_emotions:
        weight = positive_emotions[word] * count
    elif word in negative_emotions:
        weight = negative_emotions[word] * count
    elif word in neutral_keywords:
        weight = neutral_keywords[word] * count
    
    # 只保留有权重的词
    if weight != 0:
        emotion_weights[word] = abs(weight)  # 词云用绝对值表示大小

# 按权重排序
sorted_emotions = sorted(emotion_weights.items(), key=lambda x: x[1], reverse=True)

print("\n=== 情感关键词 TOP 30 ===")
for word, weight in sorted_emotions[:30]:
    # 判断情感倾向
    if word in positive_emotions:
        sentiment = "正面 😊"
    elif word in negative_emotions:
        sentiment = "负面 😢"
    else:
        sentiment = "中性 😐"
    print(f"{word:8s} | 权重: {weight:4d} | {sentiment}")

# 生成词云数据
wordcloud_data = dict(sorted_emotions[:100])  # 取前100个词

# 创建词云
wordcloud = WordCloud(
    font_path='C:/Windows/Fonts/simhei.ttf',  # Windows系统字体路径
    width=1200,
    height=800,
    background_color='white',
    max_words=100,
    colormap='viridis',  # 颜色主题
    contour_width=1,
    contour_color='steelblue',
    random_state=42
).generate_from_frequencies(wordcloud_data)

# 可视化
fig, axes = plt.subplots(1, 2, figsize=(20, 10))
fig.suptitle('抖音评论内容情感词云分析', fontsize=18, fontweight='bold', y=0.98)

# 左图：词云图
axes[0].imshow(wordcloud, interpolation='bilinear')
axes[0].axis('off')
axes[0].set_title('情感关键词词云', fontsize=14, fontweight='bold')

# 右图：TOP 20情感词柱状图
top_20_words = [x[0] for x in sorted_emotions[:20]]
top_20_weights = [x[1] for x in sorted_emotions[:20]]

# 确定每个词的情感颜色
bar_colors = []
for word in top_20_words:
    if word in positive_emotions:
        bar_colors.append('#4ECDC4')  # 青绿色 - 正面
    elif word in negative_emotions:
        bar_colors.append('#FF6B6B')  # 红色 - 负面
    else:
        bar_colors.append('#FFA07A')  # 橙色 - 中性

bars = axes[1].barh(range(len(top_20_words)), top_20_weights, color=bar_colors)
axes[1].set_yticks(range(len(top_20_words)))
axes[1].set_yticklabels(top_20_words, fontsize=11)
axes[1].set_xlabel('情感权重', fontsize=12)
axes[1].set_title('TOP 20 情感关键词权重', fontsize=14, fontweight='bold')
axes[1].grid(axis='x', alpha=0.3, linestyle='--')
axes[1].invert_yaxis()  # 让权重最高的在最上面

# 添加数值标签
for i, (bar, weight) in enumerate(zip(bars, top_20_weights)):
    axes[1].text(weight + 1, i, str(weight), va='center', fontsize=9)

# 添加图例说明
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor='#4ECDC4', label='正面情感'),
    Patch(facecolor='#FF6B6B', label='负面情感'),
    Patch(facecolor='#FFA07A', label='中性关键词')
]
axes[1].legend(handles=legend_elements, loc='lower right', fontsize=10)

plt.tight_layout()
plt.savefig('emotion_wordcloud.png', dpi=300, bbox_inches='tight')
plt.show()

print("\n=== 情感统计摘要 ===")
positive_count = sum(1 for word in filtered_words if word in positive_emotions)
negative_count = sum(1 for word in filtered_words if word in negative_emotions)
neutral_count = sum(1 for word in filtered_words if word in neutral_keywords)

total = positive_count + negative_count + neutral_count
print(f"正面情感词出现次数: {positive_count} ({positive_count/total*100:.1f}%)")
print(f"负面情感词出现次数: {negative_count} ({negative_count/total*100:.1f}%)")
print(f"中性关键词出现次数: {neutral_count} ({neutral_count/total*100:.1f}%)")

print("\n情感词云图已保存为: emotion_wordcloud.png")
