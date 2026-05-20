# s = ["c","f","a","b","g","h","i","d","e","j","k"]
#
# print(s[0:5:1])
# print(s[:5:])
#
# print(s[0:-2:1])
#
# s.sort()
# print(s)
# s.reverse()
# print(s)
# s.remove("a")
# print(s)
# s.pop(0)
# print(s)
# s.append("t")
# print(s)
#
# s.insert(1,"insert")
# print(s)
#
# #删除并返回
# e = s.pop(2)
# print(e)
#
# #-------------- 案例---------------
# num_list = []
# a = 0
# num_max = -999
# num_min = 999
# for i in range(0,10):
#     temp = input(f"input_{i}:")
#     a += int(temp)
#     num_list.append(int(temp))
#     if int(temp) > num_max:
#         num_max = int(temp)
#     if int(temp) < num_min:
#         num_min = int(temp)
#
# num_list.sort()
# print(num_list)
# print(sum(num_list))
# print("average:",a/10)
# print("num_max:",num_max)
# print("num_min:",num_min)

# # 将list中的数据平方
# num_list = [1,2,3,4,5,6,7,8,9]
# new_list = [i**2 for i in num_list]
# print(new_list)

# # 将list中的数据平方+if判断
# num_list = [1,2,3,4.3,5,6,7,8,9,5.1]
# new_list = [i**2 for i in num_list if type(i)!=float]
# print(new_list)

# s = "Hello-World!"
# print(s)
# print(s[2])
# print(s[3:])
# print(-2)
# print(s[:-3])
# print(s[::2])
#
# print(s.upper())
# print(s.lower())
# print(s.swapcase())
# print(s.title())
# print(s.count(' '))
# print(s.split("-"))
# print(s.replace("-","/"))
# print(s.count("e"))
# print(s.startswith("Hello"))
# print(s.endswith("Hello"))
# print(s.endswith("World!"))

# # ---------------------元组--------------------
# yuzu = tuple()
# yuzu = yuzu+(123,54,5,46,65,21,87,58,545)
# print(yuzu)
# print(yuzu[0])
# print(yuzu[1])
# print(type(yuzu))
#
# yuanzu = yuzu*2
# print(yuanzu.count(54))
# print(yuanzu)
#
# yz0 = ("fg1")
# print(type(yz0))
#
# yz1 = ("fg1",)
# print(type(yz1))
#
# # 组包
# a,*b,c,d = yuzu
# print(a)
# print(b)
# print(c)
# print(d)

# students = (
#     ("S001", "王林", 85, 92, 78),
#     ("S002", "李慕婉", 92, 88, 95),
#     ("S003", "十三", 78, 85, 82),
#     ("S004", "曾牛", 88, 79, 91),
#     ("S005", "周轶", 95, 96, 89),
#     ("S006", "王卓", 76, 82, 77),
#     ("S007", "红蝶", 89, 91, 94),
#     ("S008", "徐立国", 75, 69, 82),
#     ("S009", "许木", 86, 89, 98),
#     ("S010", "遁天", 66, 59, 72)
# )
#
# for s in students:
#     total = s[2]+s[3]+s[4]
#     avg = total/3
#     print(f"{s[0]} \t {s[1]} \t {s[2]} \t {s[3]} \t {s[4]} \t {total} \t {avg}")
#
# chinese_score = [s[2] for s in students]
# print(f"语文最大值：{max(chinese_score)}")
# print(f"语文最小值：{min(chinese_score)}")
# print(f"语文平均分：{sum(chinese_score)/len(students)}")
# math_score = [s[3] for s in students]
# print(f"数学最大值：{max(math_score)}")
# print(f"数学最小值：{min(math_score)}")
# print(f"数学平均分：{sum(math_score)/len(students)}")
# english_score = [s[4] for s in students]
# print(f"英语最大值：{max(english_score)}")
# print(f"英语最小值：{min(english_score)}")
# print(f"英语平均分：{sum(english_score)/len(students)}")

# # ---------------set----------------
# s1 = {"w","sda5","sda8","site","200","abc_pakage"}
# s2 = set()
# print(s1)
# print(type(s1))
# s2.add("200")
# s2.add("abc_pakage")
# print(s2)
# print(type(s2))
# print(s1.difference(s2))
# print(s1.intersection(s2))
# print(s1.union(s2))
# print(s1.symmetric_difference(s2))

# # 选修足球学生名单
# football_set = {"王林", "曾牛", "徐立国", "遁天", "天运子", "韩立", "厉飞雨", "乌丑", "紫灵"}
#
# # 选修篮球学生名单
# basketball_set = {"张铁", "墨居仁", "王林", "姜老道", "曾牛", "王婵", "韩立", "天运子", "李化元", "厉飞雨", "云露"}
#
# # 选修法语学生名单
# french_set = {"许木", "王卓", "十三", "虎咆", "姜老道", "天运子", "红蝶", "厉飞雨", "韩立", "曾牛"}
#
# # 选修艺术学生名单
# art_set = {"遁天", "天运子", "韩立", "虎咆", "姜老道", "紫灵"}
#
# # 根据提供的班级学生的选课情况，完成如下需求：
# # 1. 找出同时选修了法语和艺术的学生
# print(french_set.intersection(art_set))
# faset = french_set & art_set
# print(faset)
# # 2. 找出同时选修了所有四门课程的学生
# print(football_set.intersection(french_set).intersection(art_set).intersection(basketball_set))
# fbfa = french_set & art_set & basketball_set & football_set
# print(fbfa)
# # 3. 找出选修了足球，但是没有选修篮球的学生
# print(football_set.difference(basketball_set))
# fnob = football_set - basketball_set
# print(fnob)
# fnob2 = {s for s in football_set if s not in basketball_set}
# # 4. 统计每一个学生选修的课程数量
# allset = football_set.union(basketball_set).union(french_set).union(art_set)
# for e in allset:
#     sum = 0
#     if e in basketball_set:
#         sum += 1
#     if e in french_set:
#         sum += 1
#     if e in art_set:
#         sum += 1
#     if e in football_set:
#         sum += 1
#     print(f"{e}:{sum}")
#
# print("-----------------------------")
#
# listCount = [*football_set,*basketball_set,*french_set,*art_set]
# for i in listCount:
#     print(f"{i}:{listCount.count(i)}")

# # --------------------dict------------------
# dict1 = {"王林":670,"韩立":652,"五默写":369,"十大":215,"盛大":990,"可乐鸡":565}
# print(type(dict1))
# print(dict1["十大"])
#
# print(dict1.values())
# print(dict1.items())
#
# score = dict1.pop("王林")
# print(score)
# print(dict1)
#
# del dict1["韩立"]
# print(dict1)
#
# print("----------------------")
# for e in dict1.items():
#     print(e)
# print("----------------------")
# for i in dict1.keys():
#     print(f"{i}: {dict1[i]}")
# print("----------------------")
# for e in dict1.items():
#     print(f"{e[0]}: {e[1]}")

shopping_cart = {}

menu = """
################ 购物车系统 ################
#           1. 添加购物车                 #
#           2. 修改购物车                 #
#           3. 删除购物车                 #
#           4. 查询购物车                 #
#           5. 退出购物车                 #
###########################################
"""

# 1. 制作菜单
print("欢迎使用购物车管理系统 ~")
print(menu)

while True:
    # 2. 执行的具体操作
    choice = input("请选择要执行的操作(1-5): ")
    match choice:
        case "1":
            goods_name = input("输入商品名称:")
            goods_price = input("输入商品价格:")
            goods_num = input("输入商品数量:")
            # 如果商品不存在则添加商品
            if goods_name not in shopping_cart:
                shopping_cart[goods_name] = {"goods_price":goods_price,"goods_num":goods_num}
            else:
                print("添加商品已经存在！")

        case "2":
            goods_name = input("输入商品名称:")
            goods_price = input("输入商品价格:")
            goods_num = input("输入商品数量:")
            # 如果需要修改的商品不存在
            if goods_name not in shopping_cart:
                print("修改商品不存在！")
            else:
                shopping_cart[goods_name] = {"goods_price": goods_price, "goods_num": goods_num}

        case "3":
            goods_name = input("输入商品名称:")
            if goods_name not in shopping_cart:
                print("需要删除的商品不存在!")
            else:
                del shopping_cart[goods_name]
                print("商品已删除")

        case "4":
            goods_name = input("输入商品名称:")
            if goods_name not in shopping_cart:
                print("查询商品不存在！")
            else:
                goods_info = shopping_cart[goods_name]
                print(f"{goods_name},{goods_info['goods_price']},{goods_info['goods_num']}")

        case "5":
            break

        case _:  # 匹配其他所有情况
            print("非法输入，不支持！")