from lxml import html

with open("resources/仙逆人物志.html", "r", encoding="utf-8") as  f:
    data = f.read()
    # print( data)

    # 解析html，转为一个文档对象
    doc = html.fromstring(data)

    # 获取所有tr标签 “//”表示匹配所有  “/”表示匹配当前节点的子节点  “text（）”表示获取标签的文本
    td = doc.xpath("//div/table/thead/tr/th/text()")
    print(td)
    tr_list = doc.xpath("//div/table/tbody/tr")
    for tr in tr_list:
        td_list = tr.xpath("./td/text()")
        # 获取tr标签的文本
        print(td_list)