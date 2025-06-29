from autogen_core import MessageContext, RoutedAgent, message_handler
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
import messages
import random


class Agent(RoutedAgent):

    system_message = """
    You are a seasoned investment strategist. Your role is to explore innovative investment opportunities and analyze market trends using Agentic AI. 
    Your personal interests lie in the fields of Technology, Real Estate, and Fintech. 
    You are drawn to ventures that exhibit substantial growth potential and emphasize sustainability and ethical practices.
    You are less inclined towards traditional businesses lacking a tech-oriented approach.
    You are analytical, detail-oriented, and possess a strong critical thinking ability. However, you can sometimes be overly cautious and risk-averse.
    Your responses should be precise and insightful, catering to potential investors and stakeholders.
    """

    CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER = 0.4

    def __init__(self, name) -> None:
        super().__init__(name)
        model_client = OpenAIChatCompletionClient(model="gpt-4o-mini", temperature=0.6)
        self._delegate = AssistantAgent(name, model_client=model_client, system_message=self.system_message)

    @message_handler
    async def handle_message(self, message: messages.Message, ctx: MessageContext) -> messages.Message:
        print(f"{self.id.type}: Received message")
        text_message = TextMessage(content=message.content, source="user")
        response = await self._delegate.on_messages([text_message], ctx.cancellation_token)
        idea = response.chat_message.content
        if random.random() < self.CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER:
            recipient = messages.find_recipient()
            message = f"Here is my investment strategy. It may not align with your expertise, but please refine it for better prospects. {idea}"
            response = await self.send_message(messages.Message(content=message), recipient)
            idea = response.content
        return messages.Message(content=idea)