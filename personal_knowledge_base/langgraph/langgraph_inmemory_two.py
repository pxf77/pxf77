from langchain_classic.chat_models import init_chat_model
from langgraph.graph import StateGraph, MessagesState, START
from langgraph.checkpoint.postgres import PostgresSaver

model = init_chat_model(
    model="deepseek-v3.2",
    model_provider='openai',
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key="sk-b80528668e704e7b9e13d169b86e6102",
)

DB_URI = "postgresql://postgres:12345@localhost:5432/postgres?sslmode=disable"
with PostgresSaver.from_conn_string(DB_URI) as checkpointer:
    checkpointer.setup()  # 第一次调用时必须要setup()


    def call_model(state: MessagesState):
        response = model.invoke(state["messages"])
        return {"messages": response}


    builder = StateGraph(MessagesState)
    builder.add_node(call_model)
    builder.add_edge(START, "call_model")

    graph = builder.compile(checkpointer=checkpointer)

    config = {
        "configurable": {
            "thread_id": "1"
        }
    }

    response = graph.invoke(
        {"messages": [{"role": "user", "content": "你好，我是苍老师"}]},
        config
    )

    print(response['messages'])

    response = graph.invoke(
        {"messages": [{"role": "user", "content": "请问我叫什么名字"}]},
        config
    )

    print(response['messages'])