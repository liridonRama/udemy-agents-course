import gradio as gr
from dotenv import load_dotenv
from research_manager_agent import run

load_dotenv(override=True)


async def research_chat(message: str, history: list) -> str:
    """Simple chat function that processes research queries"""
    try:
        message_history = []
        for user_msg, assistant_msg in history:
            message_history.extend(
                [
                    {"role": "user", "content": user_msg},
                    {"role": "assistant", "content": assistant_msg},
                ]
            )
        message_history.append({"role": "user", "content": message})

        response = await run(message_history)

        return response

    except Exception as e:
        return f"Error during research: {str(e)}"


ui = gr.ChatInterface(
    fn=research_chat,
    title="🔍 Deep Research Chat",
    description="Ask research questions and build upon previous conversations. Chat history is automatically maintained.",
    theme=gr.themes.Default(primary_hue="sky"),
)

if __name__ == "__main__":
    ui.launch(inbrowser=True)
