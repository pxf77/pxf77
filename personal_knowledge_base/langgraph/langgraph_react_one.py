from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from langchain_classic.chat_models import init_chat_model
from langgraph.constants import START

class State(TypedDict):
    messages: Annotated[list, add_messages]

graph_builder = StateGraph(State)

model = init_chat_model(
    model="deepseek-v3.2",
    model_provider='openai',
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key="sk-b80528668e704e7b9e13d169b86e6102",
)

def chatbot(state: State):
    return {"messages": [model.invoke(state["messages"])]}

# 添加节点
graph_builder.add_node("chatbot", chatbot)

# 添加边
graph_builder.add_edge(START, "chatbot")

graph = graph_builder.compile()
# 单轮对话
# final_state = graph.invoke({"messages": ["你好，我叫陈明，好久不见。"]})
# print(final_state['messages'])

# 多轮对话
from langchain_core.messages import AIMessage, HumanMessage
messages_list = [
    HumanMessage(content="你好，我叫大模型真好玩，好久不见。"),
    AIMessage(content="你好呀！我是苍老师，是一名女演员。很高兴认识你！"),
    HumanMessage(content="请问，你还记得我叫什么名字么？"),
]
final_state = graph.invoke({"messages": messages_list})
print(final_state['messages'])