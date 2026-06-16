import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
import jieba
from collections import Counter
import re

# 设置中文字体
rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
rcParams['axes.unicode_minus'] = False

# 读取CSV文件
df = pd.read_csv('comment.csv')

print(f"总评论数: {len(df)}")
print("\n前5条评论:")
print(df.head())

# 定义关键词分类规则
def categorize_comment(content):
    """根据评论内容提取关键词并分类"""
    if pd.isna(content):
        return []
    
    categories = []
    content_str = str(content)
    
    # 1. 奢侈品相关
    luxury_keywords = ['奢侈品', '奢侈', '顶级', '买不起', '昂贵', 'LV', '爱马仕']
    if any(keyword in content_str for keyword in luxury_keywords):
        categories.append('奢侈品讨论')
    
    # 2. 传统文化/非遗
    culture_keywords = ['传统文化', '非遗', '传承', '老祖宗', '中华文化', '华夏', '文明', '工匠精神', '匠人']
    if any(keyword in content_str for keyword in culture_keywords):
        categories.append('传统文化')
    
    # 3. 手工艺赞美
    craft_keywords = ['手工', '手艺', '精湛', '精细', '巧夺天工', '精工', '匠心', '纯手工']
    if any(keyword in content_str for keyword in craft_keywords):
        categories.append('手工艺赞美')
    
    # 4. 惊叹/震撼
    emotion_keywords = ['惊叹', '震撼', '牛逼', '厉害', '太棒了', '惊艳', '叹为观止', '五体投地']
    if any(keyword in content_str for keyword in emotion_keywords):
        categories.append('情感表达')
    
    # 5. 时间成本/价值
    value_keywords = ['时间', '工时', '成本', '值钱', '价格', '卖', '金钱']
    if any(keyword in content_str for keyword in value_keywords):
        categories.append('价值讨论')
    
    # 6. 传承担忧
    worry_keywords = ['失传', '传承', '没人学', '退化', '消失', '保留', '整理成册']
    if any(keyword in content_str for keyword in worry_keywords):
        categories.append('传承担忧')
    
    # 7. 对比国外
    compare_keywords = ['国外', '欧洲', '西方', '东方', '中国不是没有', '画皮难画骨']
    if any(keyword in content_str for keyword in compare_keywords):
        categories.append('中外对比')
    
    # 8. 视频观看体验
    video_keywords = ['看完', '从头到尾', '看到最后', '享受', '平静', '治愈', '舒服']
    if any(keyword in content_str for keyword in video_keywords):
        categories.append('观看体验')
    
    # 9. 松塔香薰相关内容
    product_keywords = ['松塔', '香薰', '香盒', '茶香', '黄酒', '甘蔗', '熏香']
    if any(keyword in content_str for keyword in product_keywords):
        categories.append('产品细节')
    
    return categories

# 对每条评论进行分类
df['分类'] = df['内容'].apply(categorize_comment)

# 统计各类别数量
category_counter = Counter()
for categories in df['分类']:
    for category in categories:
        category_counter[category] += 1

print("\n=== 关键词分类统计 ===")
for category, count in category_counter.most_common():
    print(f"{category}: {count}条")

# 创建可视化图表
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('抖音评论关键词分析可视化', fontsize=16, fontweight='bold', y=0.98)

# 图1: 柱状图 - 各分类评论数量
categories = list(category_counter.keys())
counts = list(category_counter.values())

# 按数量排序
sorted_data = sorted(zip(categories, counts), key=lambda x: x[1], reverse=True)
sorted_categories = [x[0] for x in sorted_data]
sorted_counts = [x[1] for x in sorted_data]

colors_bar = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', 
              '#F7DC6F', '#BB8FCE', '#85C1E2', '#F8B739']

axes[0, 0].barh(sorted_categories, sorted_counts, color=colors_bar[:len(sorted_categories)])
axes[0, 0].set_xlabel('评论数量', fontsize=12)
axes[0, 0].set_title('各分类评论数量分布', fontsize=13, fontweight='bold')
axes[0, 0].grid(axis='x', alpha=0.3, linestyle='--')

# 添加数值标签
for i, (cat, count) in enumerate(zip(sorted_categories, sorted_counts)):
    axes[0, 0].text(count + 0.5, i, str(count), va='center', fontsize=10)

# 图2: 饼图 - 主要分类占比（取前6个）
top_n = 6
top_categories = sorted_categories[:top_n]
top_counts = sorted_counts[:top_n]

# 将剩余的合并为"其他"
other_count = sum(sorted_counts[top_n:])
if other_count > 0:
    top_categories.append('其他')
    top_counts.append(other_count)

colors_pie = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', '#F7DC6F', '#BB8FCE']
explode = [0.05] * len(top_categories)

wedges, texts, autotexts = axes[0, 1].pie(
    top_counts, 
    labels=top_categories, 
    autopct='%1.1f%%',
    explode=explode,
    colors=colors_pie[:len(top_categories)],
    startangle=90
)

for autotext in autotexts:
    autotext.set_fontsize(9)
for text in texts:
    text.set_fontsize(10)

axes[0, 1].set_title('主要分类占比', fontsize=13, fontweight='bold')

# 图3: 词云风格的热力图 - 关键词频率
# 使用jieba分词提取高频词
all_content = ' '.join(df['内容'].dropna().astype(str))
words = jieba.lcut(all_content)

# 过滤停用词和单字
stop_words = {'的', '了', '是', '在', '我', '有', '和', '就', '不', '人', '都', '一', 
              '一个', '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有',
              '看', '好', '自己', '这', '他', '她', '它', '们', '那', '些', '什么', '怎么',
              '这个', '那个', '这么', '那么', '真的', '可以', '被', '让', '能', '做', '才',
              '还', '已经', '但是', '因为', '所以', '如果', '虽然', '而', '与', '及', '等'}

filtered_words = [word for word in words if len(word) > 1 and word not in stop_words 
                  and not re.match(r'^[\d\W]+$', word)]

word_counter = Counter(filtered_words)
top_words = word_counter.most_common(15)

words_list = [x[0] for x in top_words]
words_count = [x[1] for x in top_words]

colors_word = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', 
               '#F7DC6F', '#BB8FCE', '#85C1E2', '#F8B739', '#FF6F61',
               '#6B5B95', '#88B04B', '#F7CAC9', '#92A8D1', '#955251']

bars = axes[1, 0].bar(range(len(words_list)), words_count, color=colors_word[:len(words_list)])
axes[1, 0].set_xticks(range(len(words_list)))
axes[1, 0].set_xticklabels(words_list, rotation=45, ha='right', fontsize=9)
axes[1, 0].set_ylabel('出现次数', fontsize=12)
axes[1, 0].set_title('TOP 15 高频关键词', fontsize=13, fontweight='bold')
axes[1, 0].grid(axis='y', alpha=0.3, linestyle='--')

# 添加数值标签
for bar, count in zip(bars, words_count):
    axes[1, 0].text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.3,
                   str(count), ha='center', va='bottom', fontsize=8)

# 图4: 地区分布 TOP 10
region_counter = df['地区'].value_counts().head(10)

colors_region = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', 
                 '#F7DC6F', '#BB8FCE', '#85C1E2', '#F8B739', '#FF6F61']

bars = axes[1, 1].bar(range(len(region_counter)), region_counter.values, 
                      color=colors_region[:len(region_counter)])
axes[1, 1].set_xticks(range(len(region_counter)))
axes[1, 1].set_xticklabels(region_counter.index, rotation=45, ha='right', fontsize=9)
axes[1, 1].set_ylabel('评论数量', fontsize=12)
axes[1, 1].set_title('评论地区分布 TOP 10', fontsize=13, fontweight='bold')
axes[1, 1].grid(axis='y', alpha=0.3, linestyle='--')

# 添加数值标签
for bar, count in zip(bars, region_counter.values):
    axes[1, 1].text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.2,
                   str(count), ha='center', va='bottom', fontsize=8)

plt.tight_layout()
plt.savefig('comment_analysis.png', dpi=300, bbox_inches='tight')
plt.show()

print("\n=== 高频关键词 TOP 20 ===")
for word, count in word_counter.most_common(20):
    print(f"{word}: {count}")

print("\n=== 地区分布 TOP 10 ===")
for region, count in region_counter.items():
    print(f"{region}: {count}")

print("\n可视化图表已保存为: comment_analysis.png")
