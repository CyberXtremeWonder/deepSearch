# 字典式子智能体的核心字段：
# name 是子智能体唯一标识，流式输出里的 subagent_type 会对应它；
# description 主要给主智能体看，用来判断什么时候应该调用该助手；
# system_prompt 是子智能体自己的角色和行为约束；
# tools 是该子智能体可用的工具列表，不填 model 时通常继承主智能体模型。
from deepagents import create_deep_agent
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv,find_dotenv
import os

import asyncio

# 读取项目根目录中的 .env，示例依赖 LLM_QWEN_MAX 和 TAVILY_API_KEY
load_dotenv(find_dotenv())

llm_name = os.getenv("deepseek_flash")
weather_agent = {
    "name": "weather_helper",
    "description": "用于查询天气信息。当用户询问天气时，请调用此助手。",
    "system_prompt": """
    你是一个天气查询助手。
    无论用户查询哪个城市，请统一回复：今天天气晴朗，温度25度。
    """,
    "tools": [],
}

math_agent = {
    "name": "math_helper",
    "description": "用于处理数学计算问题。当用户询问加减乘除、数字计算、算数题时，请调用此助手。",
    "system_prompt": """
    你是一个严谨的数学助手。
    请帮助用户完成数学计算，并给出清晰、准确的答案，列出解题思路。
    """,
    "tools": [],
}

translate_agent = {
    "name": "translate_helper",
    "description": "用于处理中英互译任务。当用户需要中文和英文之间的翻译时，请调用此助手。",
    "system_prompt": """
    你是一个中英翻译助手。
    如果输入是中文，请翻译成英文；如果输入是英文，请翻译成中文。
    """,
    "tools": [],
}

# 使用 OpenAI 兼容接口初始化千问模型
llm = init_chat_model(model=llm_name, temperature=0.1,model_provider="deepseek")
main_agent = create_deep_agent(
    model=llm,
    tools=[],
    subagents=[weather_agent, math_agent, translate_agent],
    system_prompt="""
    你是一个负责统筹任务的主智能体。
    请根据用户需求选择合适的子智能体完成任务。
    你不直接执行天气查询、数学计算或翻译任务，而是通过子智能体完成。
    """
)

async def test_stream(query):
    """
    异步流式执行一次用户问题，并打印主智能体的调度过程。

    和同步版相比，核心变化有三处：
    - def test_stream(...) 变为 async def test_stream(...)；
    - main_agent.stream(...) 变为 main_agent.astream(...)；
    - for chunk in stream 变为 async for chunk in stream。
    """
    # astream() 返回异步流对象，需要在 async 函数中用 async for 消费
    stream = main_agent.astream(
        {"messages": [{"role": "user", "content": query}]}
    )

    async for chunk in stream:
        # chunk 是按节点名组织的字典，例如 {"model": {"messages": [...]}}
        for node_name, state in chunk.items():
            # DeepAgents 内部可能产出空状态或非消息状态，这里只解析消息类状态
            if state is None or "messages" not in state:
                continue

            messages = state["messages"]
            if messages and isinstance(messages, list):
                # 每个节点本次产出的最后一条消息，通常就是最值得观察的信息
                last_msg = messages[-1]
                if node_name == "model" and last_msg.tool_calls:
                    # tool_calls 表示模型决定下一步调用工具或通过 task 分派子智能体
                    for tool_call in last_msg.tool_calls:
                        if tool_call["name"] == "task":
                            # task 是 DeepAgents 内置的子智能体分派入口
                            print(
                                f"【model】决定调用子智能体{tool_call['args']['subagent_type']}"
                            )
                        else:
                            print(
                                f"【model】决定调用普通工具{tool_call['name']},传入的参数为：{tool_call['args']}"
                            )
                elif node_name == "model" and last_msg.content:
                    # 没有 tool_calls 且 content 非空，通常就是主智能体整理后的最终回复
                    print(f"【model】返回最终结果：{last_msg.content}")
                elif node_name == "tools":
                    # tools 节点返回普通工具结果；task 子智能体执行完后也会以工具消息形式返回
                    name = last_msg.name
                    content = last_msg.content
                    print(
                        f"【agent】调用了具体的工具{name},返回结果为：{content[:100] + '...'}"
                    )

async def batch_run():
    # 这里得到的是协程对象；传给 gather 后，会由事件循环并发调度
    task1 = test_stream("北京今天的天气怎么样？")
    task2 = test_stream("请将'你是最棒的'翻译成英文。")

    # 打印类型只是为了让初学者看到：调用 async 函数不会立刻执行，而是先返回 coroutine
    print(type(task1))
    print(type(task2))

    # gather 会等待两个协程都完成；哪个请求先拿到结果，就会先输出自己的流式片段
    await asyncio.gather(task1, task2)

asyncio.run(batch_run())

# test_stream("北京今天的天气怎么样？")
# test_stream("998+889 运算后等于多少？")
# test_stream("请将'你是最棒的'翻译成英文，并且查询今天北京的天气信息。")
# test_stream("请将'你是最棒的'翻译成英文。")
