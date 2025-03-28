import streamlit as st
from utils import dataframe_agent
import pandas as pd

def create_chart(input_data,chart_type):
    df_data = pd.DataFrame(input_data["data"],columns=input_data["columns"],)
    df_data.set_index(input_data["columns"][0],inplace=True)
    if chart_type == "bar":
        st.bar_chart(df_data)
    if chart_type == "line":
        st.line_chart(df_data)
    if chart_type == "scatter":
        st.scatter_chart(df_data)

st.title("Chilli的Csv智能数据分析工具")

with st.expander('''这是一个Csv数据分析工具，该工具能够实现关于用户上传的Csv表格中数据信息的问答，还能够实现对数
据表格中的信息进行提取，以及把数据表格中内容进行可视化的功能'''):

    with st.sidebar:
        openai_api_key = st.text_input("请输入Openai Api Key:",type="password")
        st.markdown("[获取OpenAI API key](https://platform.openai.com/account/api-keys)")

data = st.file_uploader("请上传你的数据文件（CSV格式）",type=["csv"])

#判断是否上传文件，把文件储存至会话状态
if data:
    st.session_state["df"] = pd.read_csv(data)
    with st.expander("原始数据"):
        st.dataframe(st.session_state["df"])

query = st.text_area("请输入你关于以上表格的问题，或数据提取请求，或可视化要求（支持散点图、折线图、条形图）：")
button = st.button("生成回答")

if button and not openai_api_key:
    st.info("请输入你的OpenAI API密钥")
if button and "df" not in st.session_state:
    st.info("请先上传数据文件")
if button and openai_api_key and "df" in st.session_state:
    with st.spinner("AI正在思考中，请稍等..."):
        response_dict = dataframe_agent(
            openai_api_key=openai_api_key,
            df=st.session_state["df"],
            query=query
        )
    #对response_dict返回的查询结果的类型做判断
    #若返回的为table，使用DataFrame；
    #若返回的为bar、line、scatt，通过定义create_chart函数，传入response_dict和chart_type。
    if "answer" in response_dict:
        st.write(response_dict["answer"])
    if "table" in response_dict:
        st.table(pd.DataFrame(response_dict["table"]["data"],
                              columns=response_dict["table"]["columns"]))
    if "bar" in response_dict:
        create_chart(response_dict["bar"],"bar")
    if "line" in response_dict:
        create_chart(response_dict["line"], "line")
    if "scatter" in response_dict:
        create_chart(response_dict["scatter"], "scatter")



