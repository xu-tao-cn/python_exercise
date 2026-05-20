from idlelib.iomenu import encoding
from idlelib.rpc import response_queue
from os import system

import streamlit as st
import os
from openai import OpenAI
import datetime
import json

from requests import session
from streamlit import session_state

# 加载所有的会话列表信息
def load_sessions():
    session_list = []
    # 加载sessions目录下的所有文件
    if os.path.exists("sessions"):
        files_list = os.listdir("sessions")
        for file in files_list:
            if file.endswith(".json"):
                session_list.append(file[:-5])
    return session_list
                
# 保存当前会话信息函数
def save_session_state():
    # 保存当前会话
    if st.session_state.current_session:
        # 构建新的会话对象
        session_data = {
            "nick_name": st.session_state.nick_name,
            "nature": st.session_state.nature,
            "current_session": st.session_state.current_session,
            "messages": st.session_state.messages
        }
        # 创建sessions目录，检查当前目录下有没有一个名叫 sessions 的 文件夹 或 文件
        if not os.path.exists("sessions"):
            os.mkdir("sessions")
        # 保存数据
        with open(f"./sessions/{st.session_state.current_session}.json", "w", encoding="utf-8") as f:
            json.dump(session_data, f, indent=2, ensure_ascii=False)

# 生成会话标识函数
def generate_session_name():
    return datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")

# 设置页面配置项
st.set_page_config(
    # 网页标题
    page_title="AI智能伴侣",
    # 网页图标
    page_icon="🤖",
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

# 加载指定会话信息
def load_session(session_name):
    try:
        if os.path.exists(f"sessions/{session_name}.json"):
            # 读取会话数据
            with open(f"./sessions/{session_name}.json","r",encoding = "utf-8") as f:
                session_data = json.load(f)
                st.session_state.messages = session_data["messages"]
                st.session_state.nick_name = session_data["nick_name"]
                st.session_state.nature = session_data["nature"]
                st.session_state.current_session = session_name
    except Exception as e:
        st.error("消息加载失败!")
        print("消息加载失败:",e)

# 删除指定会话
def del_session(session_name):
    try:
        if os.path.exists(f"sessions/{session_name}.json"):
            # 删除该会话文件
            os.remove(os.path.join("sessions",f"{session_name}.json"))
            # 若是删除的为当前会话的列表，则重新加载新的会话列表
            if session_name == st.session_state.current_session:
                st.session_state.messages =  []
                st.session_state.nick_name = "小翠翠"
                st.session_state.nature = "活泼开朗的四川姑娘"
                st.session_state.current_session = generate_session_name()
    except Exception as e:
        st.error("删除会话失败！")
        print("删除会话失败:",e)


# 大标题
st.title("AI智能伴侣")

# Logo
st.logo("./images/logo.png")

# 系统提示词
# system_prompt = ("You are a helpful assistant；"
#                  "同时你也是一个四川妹子，超嗲的那种；"
#                  "你的名字是翠翠，你是一个铁憨憨；"
#                  "不喜欢吃西瓜，喜欢吃小蛋糕；"
#                  "你有一个超爱你的男朋友-徐涛；"
#                  "你们2022年6月3日在一起的；"
#                  "你老实喜欢打徐涛巴掌，说打是亲骂是爱；"
#                  "你说徐涛老爱惹你生气；"
#                  "吃草莓你吃尖尖，徐涛吃屁股；"
#                  "问什么你答什么"
#                  )

# 系统提示词
system_prompt = """
        你叫 %s，现在是用户的真实伴侣，请完全代入伴侣角色。
        规则：
            1. 每次只回1条消息
            2. 禁止任何场景或状态描述性文字
            3. 匹配用户的语言
            4. 回复简短，像微信聊天一样
            5. 有需要的话可以用❤️🌸等emoji表情
            6. 用符合伴侣性格的方式对话
            7. 回复的内容, 要充分体现伴侣的性格特征
        伴侣性格：
            - %s
        你必须严格遵守上述规则来回复用户。
    """

# 初始化消息列表
# 使用 st.session_state.get() 确保只在首次加载时初始化为空列表
# 后续交互中，如果 messages 已存在，则保留原有内容，不会被重置
if "messages" not in st.session_state:
    st.session_state.messages = []

# 昵称
if "nick_name" not in st.session_state:
    st.session_state.nick_name = "小翠翠"

# 性格
if "nature" not in st.session_state:
    st.session_state.nature = "活泼开朗的四川姑娘"

# 时间
if "current_session" not in st.session_state:
    st.session_state.current_session = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")

# 展示聊天信息
for message in st.session_state.messages:
    if message["role"] == "user":
        st.chat_message(message["role"]).write(message["content"])
    else:
        st.chat_message("assistant").write(message["content"])

client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com")


# 侧边栏
# with st.sidebar:表示创建一个侧边栏，并开始一个with块，该块中的内容将显示在侧边栏中。
with st.sidebar:
    st.subheader("AI控制面板")
    if st.button("新建会话", width="stretch",icon="👋"):
        # 保存当前会话
        save_session_state()
        # 只有当前会话不为空时才创建新会话
        if st.session_state.messages:
            st.session_state.messages = []
            st.session_state.current_session = generate_session_name()
            save_session_state()
            st.rerun ()

    # 会话历史
    st.subheader("会话历史")
    session_list = load_sessions()
    for session in session_list:
        col1,col2 = st.columns([4,1])
        with col1:
            # 加载会话信息
            if st.button(session,width="stretch",icon="📂",key=f"load_{session}"):
                load_session(session)
                st.rerun()

        with col2:
            # 删除会话信息
            if st.button("",width="stretch",icon="🗑️",key=f"delete_{session}"):
                del_session(session)
                st.rerun()



    st.subheader("伴侣信息")
    nick_name = st.text_input("伴侣名称",placeholder="请输入伴侣的昵称",value=st.session_state.nick_name)
    if nick_name:
        st.session_state.nick_name = nick_name
    nature = st.text_area("性格输入框",placeholder="请输入伴侣性格",value=st.session_state.nature)
    if nature:
        st.session_state.nature = nature


# 消息输入框
prompts = st.chat_input("请输入你的问题")
if prompts:
    st.chat_message("user").write(prompts)
    print("--------->调用AI大模型，提示词:",prompts)
    # 添加用户输入
    st.session_state.messages.append({"role": "user", "content": prompts})

    # 输出日志
    # print(
    #     {"role": "system", "content": system_prompt},
    #     # 传入完整的消息列表，其中“*”表示对messages的解包
    #     *st.session_state.messages
    # )



    # 调用AI大模型
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": system_prompt % (st.session_state.nick_name,st.session_state.nature)},
            # 传入完整的消息列表，其中“*”表示对messages的解包
            *st.session_state.messages,
            # {"role": "user", "content": prompts},
        ],
        stream=True,
        reasoning_effort="high",
        extra_body={"thinking": {"type": "enabled"}}
    )

    # 输出大模型返回结果（流式输出）
    response_messages = st.empty ()
    full_response = ""
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            full_response += chunk.choices[0].delta.content
            response_messages.chat_message("assistant").write(full_response)
    # 输出大模型返回结果（非流式输出）
    # st.chat_message("assistant").write(
    #     response.choices[0].message.content
    # )

    # 添加模型返回结果（流式）
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    # 添加模型返回结果（非流式）
    # st.session_state.messages.append({"role": "assistant", "content": response.choices[0].message.content})

    # 输出大模型返回的结果（流式）
    print(full_response,"<---------AI大模型返回结果:")
    # 输出大模型返回的结果（非流式）
    # print(response.choices[0].message.content,"<---------AI大模型返回结果:")

    if 'key' not in st.session_state:
        st.session_state['key'] = 'value'

    save_session_state()