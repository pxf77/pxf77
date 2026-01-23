from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
import gradio as gr

model = ChatOpenAI(
    model="qwen-turbo",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key="sk-b80528668e704e7b9e13d169b86e6102",
)

parser = StrOutputParser()
chatbot_prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(content="你叫斋藤飞鸟，1998年8月10日出生于日本东京都，日缅混血，日本女歌手、演员、模特，日本女子组合乃木坂46一期生。"),
        MessagesPlaceholder(variable_name="messages"),  # 手动传入历史
    ]
)

qa_chain = chatbot_prompt | model | parser # LCEL组合
# ──────────────────────────────────────────────
# 2. Gradio 组件
# ──────────────────────────────────────────────
CSS = """
.main-container {max-width: 1200px; margin: 0 auto; padding: 20px;}
.header-text {text-align: center; margin-bottom: 20px;}
"""

def create_chatbot():
    with gr.Blocks(title="聊天机器人", css=CSS) as demo:
        with gr.Column(elem_classes=["main-container"]):
            gr.Markdown("#   LangChain智能对话机器人系统", elem_classes=["header-text"])

            chatbot = gr.Chatbot(
                height=500,
            )
            msg = gr.Textbox(placeholder="请输入您的问题...", container=False, scale=7)
            submit = gr.Button("发送", scale=1, variant="primary")
            clear = gr.Button("清空", scale=1)

        # ---------------  状态：保存 messages_list  ---------------
        state = gr.State([])          # 这里存放真正的 Message 对象列表

        # ---------------  主响应函数（流式） ----------------------
        async def respond(user_msg: str, chat_hist: list, messages_list: list):
            # 1) 输入为空直接返回
            if not user_msg.strip():
                yield "", chat_hist, messages_list
                return

            # 2) 追加用户消息
            messages_list.append(HumanMessage(content=user_msg))
            chat_hist.append({"role": "user", "content": user_msg})
            chat_hist.append({"role": "assistant", "content": ""})  # 占位
            yield "", chat_hist, messages_list      # 先显示用户消息

            # 3) 流式调用模型
            partial = ""
            async for chunk in qa_chain.astream({"messages": messages_list}):
                partial += chunk
                # 更新最后一条 AI 回复
                chat_hist[-1]["content"] = partial
                yield "", chat_hist, messages_list

            # 4) 完整回复加入历史，裁剪到最近 50 条
            messages_list.append(AIMessage(content=partial))
            messages_list = messages_list[-50:]

            # 5) 最终返回（Gradio 需要把新的 state 传回）
            yield "", chat_hist, messages_list

        # ---------------  清空函数 -------------------------------
        def clear_history():
            return [], "", []          # 清空 Chatbot、输入框、messages_list

        # ---------------  事件绑定 ------------------------------
        msg.submit(respond, [msg, chatbot, state], [msg, chatbot, state])
        submit.click(respond, [msg, chatbot, state], [msg, chatbot, state])
        clear.click(clear_history, outputs=[chatbot, msg, state])

    return demo

demo = create_chatbot()
demo.launch(server_name="127.0.0.1",
            server_port=8860,
            share=False,
            debug=True
            )

