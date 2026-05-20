# 学生类
from random import choice


class Student:
    def __init__(self, name, chinese, math, english):
        self.name = name
        self.chinese = chinese
        self.math = math
        self.english = english

    def __str__(self):
        return f"姓名:{self.name} | 语文:{self.chinese} | 数学:{self.math} | 英语:{self.english}"

    def update_score(self,chinese=None,math=None,english=None):
        if chinese is not None:
            self.chinese = chinese
        if math is not None:
            self.math = math
        if english is not None:
            self.english = english

# if __name__ == '__main__':
#     s1 = Student("徐涛",99,110,73)
#     print(s1)
#
#     s1.update_score(95)
#     print(s1)


# 教务系统管理类
class EduManagement:
    system_version = "1.0"
    system_name = "教务管理系统"
    def __init__(self):
        self.studentsList = [] #学生成绩列表信息

    # 添加学生成绩
    def add_student(self):
        name = input("请输入添加学生姓名:")

        # 判断学生是否已经存在
        for stu in self.studentsList:
            if name == stu.name:
                print("学生已经存在")
                return

        chinese = int(input("请输入添加学生语文成绩:"))
        math = int(input("请输入添加学生数学成绩:"))
        english = int(input("请输入添加学生英语成绩:"))

        stu = Student(name, chinese, math, english)
        self.studentsList.append(stu)
        print("添加成功")

    # 修改学生成绩
    def update_student(self):
        name = input("输入需要修改的学生姓名:")
        for stu in self.studentsList:
            if name == stu.name:
                chinese = int(input("请输入修改学生语文成绩:"))
                math = int(input("请输入修改学生数学成绩:"))
                english = int(input("请输入修改学生英语成绩:"))
                stu.update_score(chinese,math,english)
                print(stu)
                return
        print("未找到该学生")
    # 删除学生成绩
    def remove_student(self):
        name = input("输入要删除学生姓名:")
        for stu in self.studentsList:
            if name == stu.name:
                self.studentsList.remove(stu)
                print("删除成功")
                return
        print("删除失败")
    # 查询学生成绩
    def query_student(self):
        name = input("查询学生姓名:")
        for stu in self.studentsList:
            if name == stu.name:
                print(stu)
                return
        print("未找到该学生")

    # 展示所有学生信息
    def list_student(self):
        for stu in self.studentsList:
            print(stu)


# 运行系统方法
    def run_system(self):
        print("welcome!")
        print("***************************************")
        print("*1添加 2修改 3删除 4查询 5展示所有信息 6退出*")
        print("***************************************")

        while True:
            choice = input("输入你的选择:")
            try:
                match choice:
                    case "1":
                        self.add_student()
                    case "2":
                        self.update_student()
                    case "3":
                        self.remove_student()
                    case "4":
                        self.query_student()
                    case "5":
                        self.list_student()
                    case "6":
                        print("Bye～")
                        return
                    # case _:
                    #     print("非法输入")
            except Exception as e:
                print("出错了:"+str(e))
            finally:
                print("-----------------------------------------")


if __name__ == '__main__':
    edu_management = EduManagement()
    edu_management.run_system()