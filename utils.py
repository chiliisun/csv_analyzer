"""
项目名称：Csv数据分析Agent
项目目标：借助Agent确保AI的回答都是实际基于上传的数据文件，根据AI在后台打印的执行流程
进行校验，该工具能够实现关于Csv数据的问答、对Csv数据的提取、Csv数据图表可视化功能
业务流程：
step1用户输入秘钥
step2用户上传Csv文件（上传）
上传文件格式限制为Csv，上传文件后数据能够在网页上以表格形式展示
step3用户查看所上传的Csv文件
表格为交互式表格，支持排序、搜索、全屏预览等操作
Step4用户提问
用户在输入框中针对Csv进行提问
"""

"""
Agent1问题回答
1）给模型发送用于理解表格内容的前几行
2）让模型思考回答问题所需的对应代码
3）最后执行代码
Agent2图表可视化
包括散点图、折线图、条形图。
1）提取房子装修状态的代码，执行代码得到各个装修状态的数量
2）把数字通过图表形式展示
Agent3提取数据

AI返回内容的格式
对表格的问题、数据提取请求、绘制图表请求，将请求传给AI，获得响应；响应的形式包括文字、表格、图表，
因此需要在提示词中制定返回内容的格式
"""
import json
from langchain_openai import ChatOpenAI
from langchain_experimental.agents import  create_pandas_dataframe_agent

Prompt_template = """
你是一位数据分析助手，你的回应内容取决于用户的请求内容。

   1.对于文字问题，按照这样的格式回答：
       {"answer":"<你的答案写在这里>"}
   例如：
       {"answer":"订单最高的产品ID是'MNWC3-067'"}
   2.如果用户需要一个表格，按照这样的格式回答：
       {"table":{"columns":["columns1","columns2",...],"data":["value1","value2",...]}}
   3.如果用户请求适合返回条形图，按照这样的格式回答：
       {"bar":{"columns":["A","B","C",...],"data":[34,21,91,...]},}
   4.如果用户请求适合返回折线图，按照这样的格式回答：
       {"line":{"columns":["A","B","C",...],"data":[34,21,91,...]}}
   5.如果用户的请求适合返回散点图，按照这样的格式回答：
       {"scatter":{"columns":["A","B","C",...],"data":[34,21,91,...]}}
   注意：只支持3种类型的图表："bar","line","scatter"。
   请将所有输出作为JSON字符串返回。同时请注意将columns和data中的字符串都用双引号包围
   例如：{"columns":["temperature","pressure"]},"data":[["54511海淀",23],["54399大兴",1024]]
   """
def dataframe_agent(openai_api_key,df,query):
    model = ChatOpenAI(
        model="gpt-4o-mini",
        openai_api_key=openai_api_key,
        base_url="https://api.aigc369.com/v1",
        temperature=0
    )
    agent = create_pandas_dataframe_agent(
        llm=model,
        df=df,
        agent_executor_kwargs={"handle_parsing_errors":True},
        verbose=True,
        allow_dangerous_code=True
    )
    prompt = Prompt_template + query
    response = agent.invoke({"input":prompt})
    # if "output" in response and response["output"]:
    #     try:
    #         print(response["output"])
    #         print(response)
    #         response_dict = json.loads(response["output"])
    #     except json.JSONDecodeError:
    #         print("警告: 返回的内容不是有效的 JSON 格式。")
    #         response_dict = {"error": "无效的 JSON 响应"}
    # else:
    #     print("警告: API 返回的内容为空。")
    #     response_dict = {"error": "API 返回的内容为空"}

    response_dict = json.loads(response["output"])
    return response_dict

