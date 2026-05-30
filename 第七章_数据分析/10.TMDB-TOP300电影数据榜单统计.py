import pandas as pd
import matplotlib.pyplot as plt

def setup_plot_style():
    """设置绘图样式以支持中文显示"""
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

def load_data(file_path='./Data/movies.csv'):
    """读取数据并处理缺失值"""
    data = pd.read_csv(file_path, usecols=['电影名', '年份', '上映时间', '类型', '时长', '评分', '语言'], dtype={'年份': 'Int64'})
    # 使用上映时间的前四位填充年份的缺失值
    data['年份'] = data['年份'].fillna(data['上映时间'].str[:4])
    return data

def plot_yearly_trend(data, ax):
    """绘制每年电影数量变化折线图"""
    year_count = data.groupby('年份')['年份'].count()
    years = [i for i in range(year_count.index.min(), year_count.index.max() + 1)]
    counts = [year_count.get(i, 0) for i in years]
    
    ax.set_xlabel('年份')
    ax.set_ylabel('电影数量')
    ax.set_title('每年电影数量变化')
    ax.set_xticks(range(min(years), max(years) + 1, 5))
    ax.set_yticks(range(0, max(counts) + 1, 2))
    ax.plot(years, counts)

def plot_language_distribution(data, ax):
    """绘制不同语言电影数量柱状图"""
    language_count = data.groupby('语言')['语言'].count().sort_values(ascending=False)
    languages = language_count.index.tolist()
    counts = language_count.values.tolist()
    
    ax.set_xlabel('语言')
    ax.set_ylabel('电影数量')
    ax.set_title('不同语言电影数量')
    ax.set_xticks(range(len(languages)))
    ax.set_yticks(range(0, max(counts) + 1, 6))
    ax.tick_params(axis='x', labelrotation=45)
    ax.bar(languages, counts, width=0.5, color='skyblue')

def plot_genre_distribution(data, ax):
    """绘制不同类型电影数量柱状图"""
    type_count = {}
    for types in data['类型'].str.split(','):
        for t in types:
            if t in type_count:
                type_count[t] += 1
            else:
                type_count[t] = 1
    
    genres = list(type_count.keys())
    counts = list(type_count.values())
    
    ax.set_xlabel('类型')
    ax.set_ylabel('电影数量')
    ax.set_title('不同类型电影数量')
    ax.tick_params(axis='x', labelrotation=45)
    ax.bar(genres, counts)

def plot_score_distribution(data, ax):
    """绘制评分比例饼图"""
    score_count = data.groupby('评分')['评分'].count()
    total = score_count.sum()
    
    # 合并占比小于2%的评分数据为“其他”
    large_score = score_count.loc[score_count >= total * 0.02]
    small_score = score_count.loc[score_count < total * 0.02]
    large_score['其他'] = small_score.sum()
    
    scores = large_score.index.tolist()
    values = large_score.values.tolist()
    
    ax.pie(values, labels=scores, autopct='%1.1f%%', startangle=0, radius=1.5)
    ax.set_title('评分比例')
    ax.legend(loc='lower center', ncol=4, bbox_to_anchor=(0.5, -0.35))

def main():
    """主函数：执行数据分析与可视化"""
    setup_plot_style()
    
    # 创建画布
    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(20, 12), dpi=100)
    fig.suptitle('TMDB电影榜单分析', fontsize=20, x=0.5, y=0.95)
    fig.subplots_adjust(wspace=0.3, hspace=0.5)
    
    # 加载数据
    data = load_data()
    
    # 绘制各个子图
    plot_yearly_trend(data, axes[0][0])
    plot_language_distribution(data, axes[0][1])
    plot_genre_distribution(data, axes[1][0])
    plot_score_distribution(data, axes[1][1])
    
    # 保存并显示图片
    plt.savefig('./Data/movies.png')
    plt.show()

if __name__ == '__main__':
    main()
