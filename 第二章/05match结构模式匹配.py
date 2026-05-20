# while 1:
#     day = input("input day:")
#     match day:
#         case "1":
#             print("work")
#         case "2":
#             print("work")
#         case "3":
#             print("work")
#         case "4":
#             print("work")
#         case "5":
#             print("work")
#         case "6":
#             print("holiday")
#         case "7":
#             print("holiday")
#         case _:#匹配其他所有输入
#             print("invalid input")
#             break


x = int(input("input x:"))#input获取的都是str类型，需要转换一下

while x < 10:
    x += 1
else:
    print("over")