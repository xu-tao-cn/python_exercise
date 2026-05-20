# def rectangle_area(width, height):
#     """
#
#     :param width: 宽度
#     :param height: 长度
#     :return: 面积
#     """
#     return width * height
#
# print(rectangle_area(5, 5))

# # 案例：计算传入字符串中元音字母个数
# def aeiou(s):
#     sum = 0
#     i = 0
#     while 1:
#         if s[i] == "a" or s[i] == "e" or s[i] == "i" or s[i] == "o" or s[i] == "u":
#             sum += 1
#         i += 1
#         if i == len(s):
#             break
#
#     return sum
#
# print(aeiou("5y8saeiAEIOUousdk215"))

# def add(x,y):
#     return x+y
#
# def calc(x,y,oper):
#     return oper(x,y)
#
# print(calc(1,3,add))

# out_line = lambda x,y:x+y
# print(out_line(1,2))

# while True:
#     def jc(n):
#         if n > 1:
#             return n * jc(n - 1)
#         else:
#             return 1
#
#
#     n = input()
#     print(jc(int(n)))

def calc_order_cost(*args: tuple[str,float,int], coupon, score, express) -> float:
    """
    根据传入的一批商品信息（商品名、价格、数量）、优惠（优惠券、积分抵扣）、运费信息计算订单的总金额
    :param args: 商品信息（商品名、价格、数量） ----> 如: ("鼠标", 188, 2) ("键盘", 388, 1)
    :param coupon: 优惠券
    :param score: 积分
    :param express: 运费
    :return: 订单的总金额
    """
    # 订单的总金额 = 商品总金额 - 优惠券 - 积分抵扣 + 运费
    # 1. 计算商品总金额
    sum = 0
    for i in range(len(args)):
        sum += int(args[i][1])*int(args[i][2])
    # 2. 扣减优惠券
    sum -= int(coupon)
    # 3. 扣减积分抵扣
    sum -= int(score)
    # 4. 添加运费
    sum += int(express)

    print(sum)
    return sum

calc_order_cost(("a",188,2),("b",288,3),("c",388,4),coupon=60,score=60,express=8)