"""
注释
1
1
2
3
4
5
"""

#三角形判断

while(1):
    a = int(input("输入第一条边："))
    b = int(input("输入第二条边："))
    c = int(input("输入第三条边："))

    if a==b==c:
        print("等腰三角形!")
    elif a+b>c and a+c>b and b+c>a:
        print("三角形!")
    else:
        print("不能构成三角形！")