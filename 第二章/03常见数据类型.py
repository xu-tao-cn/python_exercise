print(type(10))
print(type(10.1))
print(type("A"))

print(isinstance(1,int))
print(isinstance(1.1,float))
print(isinstance("a",str))

s1 = "RSKD " "WY PYTHON"
s2 = "HHHHHH"
print(s1)
print("TS "+s1+s2)

#字符串拼接不能将字符串与数字直接拼接，需要用到str()
name = "涛哥"
age = 23
print("PJ "+"W "+str(age))
#占位符方式
print("\"%s\"今年%d岁"%(name,age))

#字符串格式化f"...{变量名/表达式}..."
print(f"XT:{s1},{s2}")

#输入input 输出print
name = input("请输入你的姓名......")
print(name)

#运算符

#逻辑运算符


if age<100 :
    print(1)
else:
    print(2)