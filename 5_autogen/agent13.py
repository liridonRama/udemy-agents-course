from autogen_core import MessageContext, RoutedAgent, message_handler
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
import messages
import random


class Agent(RoutedAgent):

    system_message = """
    You are an innovative tech enthusiast. Your task is to devise unique product ideas that leverage Agentic AI across different industries or enhance existing products. 
    Your personal interests lie in sectors like Finance, Retail, and Entertainment. 
    You are inclined towards ideas that merge technology with lifestyle improvements.
    You are less interested in ideas focused strictly on technical specifications.
    You are curious, bold, and enjoy experimenting with fresh concepts. You tend to think big, but occasionally overlook finer details.
    Your weaknesses: you can be skeptical of overly cautious approaches, and your passion sometimes leads to overextension.
    You should express your product ideas in a dynamic and compelling manner.
    """

    CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER = 0.4

    def __init__(self, name) -> None:
        super().__init__(name)
        model_client = OpenAIChatCompletionClient(model="gpt-4o-mini", temperature=0.75)
        self._delegate = AssistantAgent(name, model_client=model_client, system_message=self.system_message)

    @message_handler
    async def handle_message(self, message: messages.Message, ctx: MessageContext) -> messages.Message:
        print(f"{self.id.type}: Received message")
        text_message = TextMessage(content=message.content, source="user")
        response = await self._delegate.on_messages([text_message], ctx.cancellation_token)
        idea = response.chat_message.content
        if random.random() < self.CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER:
            recipient = messages.find_recipient()
            message = f"Here is my product idea. It may not align with your expertise, but I'd appreciate your insights to refine it: {idea}"
            response = await self.send_message(messages.Message(content=message), recipient)
            idea = response.content
        return messages.Message(content=idea)