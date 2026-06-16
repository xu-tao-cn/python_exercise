from DrissionPage import ChromiumPage
from datetime import datetime
import csv
import time
import os

# 获取当前脚本所在目录
current_dir = os.path.dirname(os.path.abspath(__file__))
comment_csv_path = os.path.join(current_dir, 'comment.csv')
# alldata_csv_path = os.path.join(current_dir, 'allData.csv')
parent_dir = os.path.dirname(current_dir)
alldata_csv_path = os.path.join(parent_dir, 'allData.csv')

# 创建单独视频的csv文件
f = open(comment_csv_path, mode='w', encoding='utf-8-sig', newline='')

# 检查allData.csv是否存在，不存在则创建并写入表头
alldata_exists = os.path.exists(alldata_csv_path)
f_all = open(alldata_csv_path, mode='a', encoding='utf-8-sig', newline='')

csv_writer = csv.DictWriter(
    f,
    fieldnames=[
        '昵称',
        '地区',
        '时间',
        '内容'
    ]
)

csv_writer_all = csv.DictWriter(
    f_all,
    fieldnames=[
        '昵称',
        '地区',
        '时间',
        '内容'
    ]
)

# 如果allData.csv是新创建的，写入表头
if not alldata_exists:
    csv_writer_all.writeheader()

csv_writer.writeheader()

# 打开浏览器
dp = ChromiumPage()

# 监听评论接口
dp.listen.start('/aweme/v1/web/comment/list/')

# 打开视频
dp.get('https://www.douyin.com/video/7255314040669441299')

time.sleep(5)

# 翻页抓取
for page in range(1, 201):

    print(f'正在抓取第{page}页')

    resp = dp.listen.wait()

    json_data = resp.response.body

    comments = json_data.get('comments', [])

    for item in comments:

        nickname = item['user']['nickname']

        content = item['text']

        ip = item.get('ip_label', '未知')

        create_time = item['create_time']

        date = datetime.fromtimestamp(
            create_time
        ).strftime('%Y-%m-%d %H:%M:%S')

        data = {
            '昵称': nickname,
            '地区': ip,
            '时间': date,
            '内容': content
        }

        # 写入单独视频的csv文件
        csv_writer.writerow(data)
        
        # 追加到汇总的allData.csv文件
        csv_writer_all.writerow(data)

        print(data)

    # 滚动加载下一页评论
    dp.scroll.to_bottom()

    time.sleep(2)

f.close()
f_all.close()

print('采集完成')
print(f'单独视频数据已保存至: {comment_csv_path}')
print(f'汇总数据已追加至: {alldata_csv_path}')
