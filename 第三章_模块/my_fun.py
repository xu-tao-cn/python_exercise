# 常量(不会发生变化的数据 ; 常量的名称为全部大写)
PI = 3.1415926
NAME = "黑马☆涛哥"

# 函数
def log_separator1():  # 2用法
    print("- " * 30)  # "-"重复输出30次

def log_separator2():
    print("+ " * 30)

def log_separator3():  # 1个用法
    print("# " * 30)

def log_separator4():
    print("* " * 30)

# 测试函数
print(__name__)
if __name__ == '__main__':
    log_separator1()
