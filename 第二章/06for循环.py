# msg = input("输入需要遍历的字符串：")
#
# for s in msg:
#     print(s)
# else:
#     print("over")


"""
range(end) 获取[0，end)
range(start,end) 获取[start，end）
range(start，end，step) 获取[start,end）step个步长
"""
from random import random

# 计算1-100之间所有的奇数之和
# total = 0
# for i in range(1,101):
#     if i%2 == 1:
#         total += i
# print(total)

# 简化版
total = 0
for i in range(1,101,2):
    total += i
print(total)

m = int(input("m："))
for i in range(m):
    print("*",end='')

import random
random.randint(1,100) #生成随机数
