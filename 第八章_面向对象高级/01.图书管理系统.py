from abc import ABC,abstractmethod
from enum import member
import json

from annotated_types.test_cases import cases
from numpy.random import choice


class Book:
    def __init__(self,book_id,title,author,total_num):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.total_num = total_num
        self.__current_num = total_num

    # 借书
    def borrow_book(self):
        if self.__current_num > 0:
            self.__current_num -= 1
            print(f"借书成功，还剩{self.__current_num}本")
        else:
            print("没有可借的图书")

    # 还书
    def return_book(self):
        self.__current_num += 1
        print(f"还书成功，还剩{self.__current_num}本")

    # 获取可用书籍数量
    def get_available_num(self):
        return self.__current_num


# 抽象类，只能被继承，不能直接实例化，必须实现某些方法（带有@abstractmethod装饰器的方法）
# python中的抽象类需要继承abc中的ABC类 -> ABC:Abstractmethod Base Class
class Member(ABC):
    def __init__(self,member_id,name,password):
        self.member_id = member_id
        self.name = name
        self.__password = password
        self.__borrowed_books = []

    # 借书
    def borrow_book(self,book:Book):
        # 判断是否达到借书数量限制
        if len(self.__borrowed_books) >= self.get_max_books_num(self.member_id):
            print("借书数量已达上限")
            return False

        # 判断书籍数量是否充足
        if book.get_available_num() > 0:
            book.borrow_book()
            self.__borrowed_books.append(book)
            print("借书成功")
            return True
        else:
            print("没有可借的图书")
            return False

    # 还书
    def return_book(self,book:Book):
        #判断用户是否借了这么本书
        if book in self.__borrowed_books:
            book.return_book()
            self.__borrowed_books.remove(book)
            print(f"{self.name}还书({book.title})成功")
            # return True
        else:
            print(f"{self.name}没有借过({book.title})")
            # return False

    # 获取用户密码
    def get_password(self):
        return self.__password

    # 获取接到的书籍
    def get_borrowed_books(self):
        return self.__borrowed_books

    # 获取可借书数量
    # 必须在子类中重写
    @abstractmethod
    def get_max_books_num(self,member_id) -> int:
        pass

# 普通会员类
class NormalMember(Member):
    # 获取可借书数量
    def get_max_books_num(self,member_id) -> int:
        return 3

# VIP会员类
class VIPMember(Member):
    def __init__(self,member_id,name,password,vip_level):
        super().__init__(member_id,name,password)
        # 会员等级
        self.__vip_level = vip_level

    # 获取可借书数量
    def get_max_books_num(self,member_id) -> int:
        return 6+self.__vip_level


# 图书馆管理系统
class LibrarySystem:
    def __init__(self):
        self.books = {}
        self.members = {}
        self.currentMember : Member|None = None
        self.load_books_data()
        self.load_members_data()

    # 初始化书籍记录
    def load_books_data(self):
        books_data = json.load(open('./data/books.json','r',encoding='utf-8'))
        for book in books_data:
            # 添加数据 - 使用中文键名映射到英文参数
            self.books[book['编号']] = Book(book['编号'],book['标题'],book['作者'],book['数量'])
        print(f"加载了 {len(self.books)} 本图书")


    # 初始化会员记录
    def load_members_data(self):
        members_data = json.load(open('./data/members.json','r',encoding='utf-8'))
        for member in members_data:
            # 根据卡号前缀判断会员类型：V开头为VIP，N开头为普通会员
            if member['卡号'].startswith('V'):
                self.members[member['卡号']] = VIPMember(member['卡号'],member['姓名'],member['密码'],member['会员等级'])
            else:
                self.members[member['卡号']] = NormalMember(member['卡号'],member['姓名'],member['密码'])
        print(f"加载了 {len(self.members)} 位会员")

    def login(self):
        while True:
            member_id = input("卡号:")
            if member_id not in self.members:
                print("卡号不存在")
                continue

            password = input("密码:")
            member_info = self.members[member_id]
            # 使用 get_password() 方法获取密码，而不是字典访问
            if password != member_info.get_password():
                print("密码错误")
                continue

            print("登录成功")
            self.currentMember = member_info
            return True

    def run(self):
        if self.login():
            while True:
                print("请选择你的操作:")
                print("1:借阅图书")
                print("2:归还图书")
                print("3:查看借阅")
                print("4:退出系统")

                choice = input("请输入你的选择:")
                match choice:
                    case "1":
                        self.borrow_book()
                    case "2":
                        self.return_book()
                    case "3":
                        self.show_borrowed_books()
                    case "4":
                        self.exit_system()
                    case _:
                        print("选择错误")

    # 借书
    def borrow_book(self):
        for book in self.books:
            print(f"编号:{book.book_id} 标题:{book.title} 作者:{book.author} 数量:{book.get_available_num()}")

        choice_book_id = input("选择你要借阅书籍的编号:")
        if choice_book_id not in self.books.keys():
            print("书籍编号不存在")
            return
        self.currentMember.borrow_book(self.books[choice_book_id])

    # 归还图书
    def return_book(self):
        for book in self.currentMember.get_borrowed_books():
            print(f"编号:{book.book_id} 标题:{book.title} 作者:{book.author} 数量:{book.get_available_num()}")

        choice_book_id = input("选择你要归还的书籍的编号:")
        if choice_book_id not in self.books:
            print("书籍编号不存在")
            return
        self.currentMember.return_book(self.books[choice_book_id])

    # 显示已借阅图书
    def show_borrowed_books(self):
        for book in self.currentMember.get_borrowed_books():
            if len(self.currentMember.get_borrowed_books()) > 0:
                print(f"编号:{book.book_id} 标题:{book.title} 作者:{book.author} 数量:{book.get_available_num()}")
            else:
                print("没有借阅图书")

    # 系统
    def exit_system(self):
        pass


if __name__ == "__main__":
    library_system = LibrarySystem()
    library_system.login()