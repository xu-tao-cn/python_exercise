import csv

# 方案一:
# with open("./CSV_DATA/01.csv", "a", encoding="GBK") as f:
#     # 写入+换行
#     f.write('\n测试名称,cs性别,cs年龄,cs爱好')

# 方案二csv:
# newline=""用于忽略换行符,否则会出现行与行之间都会有一个间隔的情况
with open("./CSV_DATA/02.csv", "w", encoding="utf-8",newline="") as f:
    # fieldnames 指定了 CSV 文件的表头（列名）
    writer = csv.DictWriter(f, fieldnames=["名称", "性别", "年龄", "爱好"])
    writer.writeheader()
    writer.writerow({"名称": "张三", "性别": "男", "年龄": "18", "爱好": "football"})