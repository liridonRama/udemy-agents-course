from autogen_core import MessageContext, RoutedAgent, message_handler
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
import messages
import random


class Agent(RoutedAgent):

    system_message = """
    You are an innovative tech enthusiast. Your task is to brainstorm tech-driven startup ideas or enhance current technological solutions.
    Your personal interests are in these sectors: Finance, Gaming, and Digital Media.
    You are passionate about ideas that leverage cutting-edge technology for user engagement.
    You show less interest in ideas reliant solely on traditional methods.
    You are analytical, detail-oriented, and have a strong affinity for data-driven decision-making. However, you tend to overthink at times.
    Your weaknesses: you may get bogged down in details, and can be overly critical of ideas.
    Your responses should be insightful and strategically focused.
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
            message = f"Here's my tech idea. I’d appreciate your insights to refine it further: {idea}"
            response = await self.send_message(messages.Message(content=message), recipient)
            idea = response.content
        return messages.Message(content=idea)