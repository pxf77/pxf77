import uuid
from langchain_core.runnables import RunnableConfig
from langchain_classic.chat_models import init_chat_model
from langgraph.graph import StateGraph, MessagesState, START
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.store.postgres import PostgresStore
from langgraph.store.base import BaseStore

model = init_chat_model(
    model="deepseek-v3.2",
    model_provider='openai',
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key="sk-b80528668e704e7b9e13d169b86e6102",
)

DB_URI = "postgresql://postgres:12345@localhost:5432/postgres?sslmode=disable"

with (
    PostgresStore.from_conn_string(DB_URI) as store,
    PostgresSaver.from_conn_string(DB_URI) as checkpointer,
):
    store.setup()
    checkpointer.setup()

    def call_model(
        state: MessagesState,
        config: RunnableConfig,
        *,
        store: BaseStore,
    ):
        user_id = config["configurable"]["user_id"]
        namespace = ("memories", user_id)
        memories = store.search(namespace, query=str(state["messages"][-1].content))
        info = "\n".join([d.value["data"] for d in memories])
        system_msg = f"你是一个与人类交流的小助手，用户信息: {info}"

        last_message = state["messages"][-1]
        if "记住" in last_message.content.lower():
            memory = "用户名字是苍老师"
            store.put(namespace, str(uuid.uuid4()), {"data": memory})

        response = model.invoke(
            [{"role": "system", "content": system_msg}] + state["messages"]
        )
        return {"messages": response}

    builder = StateGraph(MessagesState)
    builder.add_node(call_model)
    builder.add_edge(START, "call_model")

    graph = builder.compile(
        checkpointer=checkpointer,
        store=store,
    )

    config = {
        "configurable": {
            "thread_id": "1",
            "user_id": "1",
        }
    }

    response = graph.invoke(
        {"messages": [{"role": "user", "content": "你好，记住: 我叫苍老师"}]},
        config
    )
    print(response['messages'][-1])

    config = {
        "configurable": {
            "thread_id": "2",
            "user_id": "1",
        }
    }

    response = graph.invoke(
        {"messages": [{"role": "user", "content": "我的名字是什么?"}]},
        config
    )
    print(response['messages'][-1])