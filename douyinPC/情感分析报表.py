import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
import jieba
from collections import Counter
import re
import os

# 设置中文字体
rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
rcParams['axes.unicode_minus'] = False

# 读取CSV文件(无表头)
df = pd.read_csv('allData.csv', header=None, names=['用户名', '地区', '时间', '内容'])

print(f"总评论数: {len(df)}")
print("\n前5条评论:")
print(df.head())

# ==================== 情感词典定义 ====================
# 正面情感词
positive_words = {
    '赞美类': ['赞', '点赞', '厉害', '牛', '牛逼', '棒', '优秀', '精彩', '完美', '精湛', '精美', 
              '惊艳', '震撼', '叹为观止', '巧夺天工', '匠心独运', '精妙', '绝妙', '出色', '卓越','奢侈品'],
    '感动类': ['感动', '流泪', '泪目', '触动', '温暖', '欣慰', '自豪', '骄傲', '敬佩', '钦佩',
              '崇拜', '敬仰', '感激', '感谢', '暖心', '治愈', '动容'],
    '喜爱类': ['喜欢', '爱', '热爱', '钟爱', '痴迷', '着迷', '陶醉', '享受', '美好', '漂亮',
              '美丽', '好看', '可爱', '温馨', '舒适', '舒服', '惬意'],
    '惊叹类': ['哇', '天哪', '不可思议', '难以置信', '惊人', '奇迹', '神奇',
              '奇妙', '非凡', '独特', '特别', '稀有', '珍贵'],
    '认同类': ['支持', '认可', '赞同', '同意', '正确', '是的', '确实', '真的', '值得',
               '必须', '重要', '意义', '价值', '传承', '发扬', '保护']
}

# 负面情感词
negative_words = {
    '担忧类': ['担心', '担忧', '忧虑', '焦虑', '害怕', '恐惧', '遗憾', '可惜', '惋惜', '失落',
              '失望', '难过', '伤心', '痛心', '心疼', '悲哀', '悲惨'],
    '批评类': ['不好', '糟糕', '错误', '问题', '缺点', '不足', '缺陷', '失败', '劣质',
              '粗糙', '低劣', '廉价', '虚假', '欺骗', '误导', '忽悠'],
    '否定类': ['拒绝', '反对', '抵制', '讨厌', '厌恶', '嫌弃',
              '反感', '不满', '抱怨', '投诉', '质疑', '怀疑']
}

# 中性/其他情感词
neutral_words = {
    '疑问类': ['什么', '怎么', '为什么', '如何', '哪里', '谁', '何时', '多少', '吗', '呢', '吧'],
    '讨论类': ['讨论', '交流', '分享', '学习', '了解', '知道', '明白', '理解', '认识', '思考',
              '研究', '探索', '发现', '观察', '体验', '感受'],
    '建议类': ['建议', '推荐', '希望', '期待', '愿望', '请求', '要求', '需要', '想要', '可以',
              '应该', '最好', '不妨', '试试', '改进', '优化']
}

# ==================== 情感分析函数 ====================
def analyze_sentiment(content):
    """对单条评论进行情感分析"""
    if pd.isna(content):
        return {'positive': [], 'negative': [], 'neutral': []}
    
    content_str = str(content)
    words = jieba.lcut(content_str)
    
    sentiment_result = {
        'positive': [],
        'negative': [],
        'neutral': []
    }
    
    for word in words:
        # 检查正面情感
        for category, word_list in positive_words.items():
            if word in word_list:
                sentiment_result['positive'].append(word)
                break
        
        # 检查负面情感
        for category, word_list in negative_words.items():
            if word in word_list:
                sentiment_result['negative'].append(word)
                break
        
        # 检查中性情感
        for category, word_list in neutral_words.items():
            if word in word_list:
                sentiment_result['neutral'].append(word)
                break
    
    return sentiment_result

# 对所有评论进行情感分析
print("\n正在进行情感分析...")
df['情感分析'] = df['内容'].apply(analyze_sentiment)

# 提取所有情感词
all_positive = []
all_negative = []
all_neutral = []

for sentiment in df['情感分析']:
    all_positive.extend(sentiment['positive'])
    all_negative.extend(sentiment['negative'])
    all_neutral.extend(sentiment['neutral'])

# 统计词频
positive_counter = Counter(all_positive)
negative_counter = Counter(all_negative)
neutral_counter = Counter(all_neutral)

print(f"\n正面情感词总数: {len(all_positive)}")
print(f"负面情感词总数: {len(all_negative)}")
print(f"中性情感词总数: {len(all_neutral)}")

# ==================== 创建可视化图表 ====================
fig = plt.figure(figsize=(20, 14))
fig.suptitle('抖音"山白"非遗短视频受众情感分析', fontsize=18, fontweight='bold', y=0.98)

# 图1: 情感分布饼图
ax1 = plt.subplot(2, 3, 1)
sentiment_counts = [len(all_positive), len(all_negative), len(all_neutral)]
sentiment_labels = ['正面情感', '负面情感', '中性情感']
colors_pie = ['#FF6B6B', '#4ECDC4', '#F7DC6F']
explode = [0.05, 0.05, 0.05]

wedges, texts, autotexts = ax1.pie(
    sentiment_counts,
    labels=sentiment_labels,
    autopct='%1.1f%%',
    explode=explode,
    colors=colors_pie,
    startangle=90
)

for autotext in autotexts:
    autotext.set_fontsize(11)
    autotext.set_fontweight('bold')
for text in texts:
    text.set_fontsize(12)

ax1.set_title('情感分布占比', fontsize=14, fontweight='bold')

# 图2: TOP 15 正面情感词
ax2 = plt.subplot(2, 3, 2)
top_positive = positive_counter.most_common(15)
if top_positive:
    pos_words = [x[0] for x in top_positive]
    pos_counts = [x[1] for x in top_positive]
    
    colors_bar = ['#FF6B6B', '#FF8E8E', '#FFA07A', '#FFB6C1', '#FFC0CB',
                  '#FFD700', '#FFE4B5', '#FFDEAD', '#FFA500', '#FF8C00',
                  '#FF7F50', '#FF6347', '#FF4500', '#FF0000', '#DC143C']
    
    bars = ax2.barh(range(len(pos_words)), pos_counts, color=colors_bar[:len(pos_words)])
    ax2.set_yticks(range(len(pos_words)))
    ax2.set_yticklabels(pos_words, fontsize=10)
    ax2.set_xlabel('出现次数', fontsize=11)
    ax2.set_title('TOP 15 正面情感词', fontsize=14, fontweight='bold')
    ax2.grid(axis='x', alpha=0.3, linestyle='--')
    
    # 添加数值标签
    for i, (word, count) in enumerate(zip(pos_words, pos_counts)):
        ax2.text(count + 0.3, i, str(count), va='center', fontsize=9)

# 图3: TOP 15 负面情感词
ax3 = plt.subplot(2, 3, 3)
top_negative = negative_counter.most_common(15)
if top_negative:
    neg_words = [x[0] for x in top_negative]
    neg_counts = [x[1] for x in top_negative]
    
    colors_neg = ['#4ECDC4', '#5FD9CA', '#6BE5D0', '#78ECD6', '#85F2DC',
                  '#92F8E2', '#9FFEE8', '#45B7D1', '#5AC2D9', '#6FCDE1',
                  '#84D8E9', '#99E3F1', '#AEEEF9', '#3AA3BA', '#2F8FA5']
    
    bars = ax3.barh(range(len(neg_words)), neg_counts, color=colors_neg[:len(neg_words)])
    ax3.set_yticks(range(len(neg_words)))
    ax3.set_yticklabels(neg_words, fontsize=10)
    ax3.set_xlabel('出现次数', fontsize=11)
    ax3.set_title('TOP 15 负面情感词', fontsize=14, fontweight='bold')
    ax3.grid(axis='x', alpha=0.3, linestyle='--')
    
    # 添加数值标签
    for i, (word, count) in enumerate(zip(neg_words, neg_counts)):
        ax3.text(count + 0.3, i, str(count), va='center', fontsize=9)

# 图4: 正面情感词分类统计
ax4 = plt.subplot(2, 3, 4)
positive_category_counter = Counter()
for category, word_list in positive_words.items():
    count = sum([positive_counter.get(word, 0) for word in word_list])
    if count > 0:
        positive_category_counter[category] = count

if positive_category_counter:
    pos_cat_data = positive_category_counter.most_common()
    pos_cat_names = [x[0].replace('类', '') for x in pos_cat_data]
    pos_cat_counts = [x[1] for x in pos_cat_data]
    
    colors_pos_cat = ['#FF6B6B', '#FF8E8E', '#FFA07A', '#FFB6C1', '#FFC0CB']
    
    bars = ax4.bar(range(len(pos_cat_names)), pos_cat_counts, color=colors_pos_cat[:len(pos_cat_names)])
    ax4.set_xticks(range(len(pos_cat_names)))
    ax4.set_xticklabels(pos_cat_names, rotation=30, ha='right', fontsize=10)
    ax4.set_ylabel('出现次数', fontsize=11)
    ax4.set_title('正面情感词分类统计', fontsize=14, fontweight='bold')
    ax4.grid(axis='y', alpha=0.3, linestyle='--')
    
    # 添加数值标签
    for bar, count in zip(bars, pos_cat_counts):
        ax4.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.5,
                str(count), ha='center', va='bottom', fontsize=9)

# 图5: 负面情感词分类统计
ax5 = plt.subplot(2, 3, 5)
negative_category_counter = Counter()
for category, word_list in negative_words.items():
    count = sum([negative_counter.get(word, 0) for word in word_list])
    if count > 0:
        negative_category_counter[category] = count

if negative_category_counter:
    neg_cat_data = negative_category_counter.most_common()
    neg_cat_names = [x[0].replace('类', '') for x in neg_cat_data]
    neg_cat_counts = [x[1] for x in neg_cat_data]
    
    colors_neg_cat = ['#4ECDC4', '#5FD9CA', '#6BE5D0']
    
    bars = ax5.bar(range(len(neg_cat_names)), neg_cat_counts, color=colors_neg_cat[:len(neg_cat_names)])
    ax5.set_xticks(range(len(neg_cat_names)))
    ax5.set_xticklabels(neg_cat_names, rotation=30, ha='right', fontsize=10)
    ax5.set_ylabel('出现次数', fontsize=11)
    ax5.set_title('负面情感词分类统计', fontsize=14, fontweight='bold')
    ax5.grid(axis='y', alpha=0.3, linestyle='--')
    
    # 添加数值标签
    for bar, count in zip(bars, neg_cat_counts):
        ax5.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.5,
                str(count), ha='center', va='bottom', fontsize=9)

# 图6: 情感强度雷达图
ax6 = plt.subplot(2, 3, 6, projection='polar')

# 计算各类别的情感强度
categories_radar = ['赞美', '感动', '喜爱', '惊叹', '认同', '担忧', '批评', '否定']
values = []

# 正面情感
for category in ['赞美类', '感动类', '喜爱类', '惊叹类', '认同类']:
    count = sum([positive_counter.get(word, 0) for word in positive_words[category]])
    values.append(count)

# 负面情感
for category in ['担忧类', '批评类', '否定类']:
    count = sum([negative_counter.get(word, 0) for word in negative_words[category]])
    values.append(count)

# 归一化到0-1范围
max_val = max(values) if values else 1
values_normalized = [v / max_val for v in values]

# 闭合雷达图
angles = [n / float(len(categories_radar)) * 2 * 3.14159 for n in range(len(categories_radar))]
angles += angles[:1]
values_normalized += values_normalized[:1]

ax6.plot(angles, values_normalized, 'o-', linewidth=2, color='#FF6B6B', label='情感强度')
ax6.fill(angles, values_normalized, alpha=0.25, color='#FF6B6B')
ax6.set_xticks(angles[:-1])
ax6.set_xticklabels(categories_radar, fontsize=10)
ax6.set_title('情感强度雷达图', fontsize=14, fontweight='bold', pad=20)
ax6.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
ax6.grid(True)

plt.tight_layout()
plt.savefig('情感分析报表.png', dpi=300, bbox_inches='tight')
plt.show()

# ==================== 输出详细统计报告 ====================
print("\n" + "="*60)
print("抖音\"山白\"非遗短视频受众情感分析报告")
print("="*60)

print(f"\n【总体统计】")
print(f"总评论数: {len(df)}")
print(f"正面情感词数量: {len(all_positive)} ({len(all_positive)/(len(all_positive)+len(all_negative)+len(all_neutral))*100:.2f}%)")
print(f"负面情感词数量: {len(all_negative)} ({len(all_negative)/(len(all_positive)+len(all_negative)+len(all_neutral))*100:.2f}%)")
print(f"中性情感词数量: {len(all_neutral)} ({len(all_neutral)/(len(all_positive)+len(all_negative)+len(all_neutral))*100:.2f}%)")

print(f"\n【TOP 20 正面情感词】")
for word, count in positive_counter.most_common(20):
    print(f"  {word}: {count}")

print(f"\n【TOP 20 负面情感词】")
for word, count in negative_counter.most_common(20):
    print(f"  {word}: {count}")

print(f"\n【正面情感词分类统计】")
for category, count in positive_category_counter.most_common():
    print(f"  {category}: {count}")

print(f"\n【负面情感词分类统计】")
for category, count in negative_category_counter.most_common():
    print(f"  {category}: {count}")

print(f"\n【情感倾向结论】")
positive_ratio = len(all_positive) / (len(all_positive) + len(all_negative)) * 100 if (len(all_positive) + len(all_negative)) > 0 else 0
if positive_ratio > 70:
    conclusion = "高度正面 - 受众对非遗文化表现出强烈的认可和喜爱"
elif positive_ratio > 50:
    conclusion = "较为正面 - 受众整体持积极态度，但存在一定担忧"
else:
    conclusion = "需要关注 - 负面情绪较多，需进一步分析原因"

print(f"  正面情感占比: {positive_ratio:.2f}%")
print(f"  结论: {conclusion}")

print("\n" + "="*60)
print("可视化图表已保存为: 情感分析报表.png")
print("="*60)
