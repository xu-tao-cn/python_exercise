import json

# 写入json数据文件
user = {
    'name': '小王',
    'age': 18,
    'sex': '男',
    'hobby': ['看电影', '看小说']
}

with open('./images/user.json', 'w', encoding='utf-8') as f:
    # 序列化
    json.dump(user, f, ensure_ascii=False, indent=2)