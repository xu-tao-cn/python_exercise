import streamlit as st

st.title("Streamlit 入门演示")
st.header("Streamlit 一级标题")
st.subheader("Streamlit 二级标题")

import streamlit as st

# 设置页面配置项
st.set_page_config(
    # 网页标题
    page_title="Ex-stream-ly Cool App",
    # 网页图标
    page_icon="🧊",
    # 整个网页布局
    layout="wide",
    # 控制侧边栏的状态
    initial_sidebar_state="expanded",
    # 菜单信息
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)

st.write("**清晨的城市还带着一层薄雾，街道上的行人不多，只有零星的车辆缓慢驶过。路边的早餐店已经开始忙碌，蒸汽从锅里不断升起，混着豆浆和油条的香气，让人瞬间清醒。**")
st.write("# 效率并不等于忙碌。很多人每天看似做了很多事情，但真正推动进展的却很少。真正的高效，是把精力集中在关键任务上，而不是被琐碎的信息不断打断。")

# 图片
st.image("./images/(P81]@3OGYHKGLZX5}]2(B5.jpg")
# 音频
st.audio("./images/music.m4a")

# 表格
datalist = {
    "labels" : ["项目A", "项目B", "项目C", "项目D", "项目E", "项目F", "项目G", "项目H", "项目I", "项目J"],
    "values" : [62, 48, 73, 55, 81, 39, 67, 59, 77, 44]
}
st.table(datalist)

mm = st.text_input("请输入密码:")
st.write("您的密码为:"+mm)

op = st.radio("选择",[
    "A",
    "B",
    "C",
    "D"
])
st.write("你的选择是:"+op)

