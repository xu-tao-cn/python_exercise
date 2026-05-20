# 打开文件
file = open("./images/望庐山瀑布.txt", "r", encoding="utf-8")

# 读取文件内容
# content = file.read()
# print(content)

content_list = file.readlines()
for content in content_list:
    print(content.strip())

# 关闭文件
file.close()

# 打开文件
file2 = open("./images/静夜诗.txt", "w", encoding="utf-8")
try:
    # 写入 文件
    file2.write("静夜诗（唐·李白）\n")
    file2.write("窗前明月光，\n")
    file2.write("疑是地上霜。\n")
    file2.write("举头望明月，\n")
    file2.write("低头思故乡。\n")
finally:
    file2.close()


with open("./images/静夜诗.txt", "w", encoding="utf-8") as file3:
    file3.write("静夜诗（唐·李白）\n")
    file3.write("窗前明月光，\n")
    file3.write("疑是地上霜。\n")
    file3.write("举头望明月，\n")
    file3.write("低头思故乡。\n")

    