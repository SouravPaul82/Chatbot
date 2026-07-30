import gradio as gr
from agent import get_agent_response

# Define custom CSS
css = """
#chatbot {
    height: 500px;
}
.gradio-container {
    max-width: 900px;
    margin: auto;
}
"""

def create_gradio_interface():
    # Pass title directly in Blocks constructor
    with gr.Blocks(title="🤖 Chatbot with Knowledge Base") as demo:
        gr.Markdown("# 🤖 Chatbot with Knowledge Base")
        
        # 'type="messages"' removed — Gradio 6 defaults to message format automatically
        history = gr.Chatbot(
            elem_id="chatbot",
            label="Chat",
            show_label=False,
            height=500,
            scale=1
        )
        
        with gr.Row():
            msg = gr.Textbox(
                label="Message",
                placeholder="Ask me anything...",
                show_label=False,
                container=False,
                scale=7
            )
            submit_btn = gr.Button("Send", variant="primary", scale=1)

        gr.ClearButton([msg, history], value="Clear Chat")

        def user_submit(message, history):
            if not message:
                return "", history
            
            history = history + [{"role": "user", "content": message}]
            return "", history

        async def call_agent(history):
            if not history or history[-1]["role"] != "user":
                return history
            
            user_message = history[-1]["content"]
            chat_history = history[:-1]
            response = await get_agent_response(user_message, chat_history)
            
            history.append({"role": "assistant", "content": response})
            return history

        # Trigger on Send button or Enter key
        submit_btn.click(user_submit, [msg, history], [msg, history]).then(
            call_agent, history, history
        )
        msg.submit(user_submit, [msg, history], [msg, history]).then(
            call_agent, history, history
        )

    return demo

if __name__ == "__main__":
    app = create_gradio_interface()
    app.launch(
        server_name="127.0.0.1",
        server_port=8080,
        share=False,
        css=css,
        show_error=True,  # Moved CSS parameter here for Gradio 6.0+
    )
