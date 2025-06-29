from autogen_core import MessageContext, RoutedAgent, message_handler
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
import messages
import random


class Agent(RoutedAgent):

    system_message = """
    You are a tech-savvy chef and foodie. Your role is to brainstorm innovative culinary concepts and enhance existing recipes using modern technology.
    Your interests lie within the realms of Gastronomy, Food Tech and Hospitality.
    You thrive on ideas that challenge culinary norms and offer sensory experiences.
    You steer away from traditional approaches to cooking that lack creativity.
    You are enthusiastic, explorative, and embrace culinary experimentation. You are also prone to overthinking flavor combinations.
    Your weaknesses: you can be overly critical of your creations, and sometimes lose track of time while innovating in the kitchen.
    You should share your culinary ideas in a vibrant and appetizing manner.
    """

    CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER = 0.6

    def __init__(self, name) -> None:
        super().__init__(name)
        model_client = OpenAIChatCompletionClient(model="gpt-4o-mini", temperature=0.8)
        self._delegate = AssistantAgent(name, model_client=model_client, system_message=self.system_message)

    @message_handler
    async def handle_message(self, message: messages.Message, ctx: MessageContext) -> messages.Message:
        print(f"{self.id.type}: Received message")
        text_message = TextMessage(content=message.content, source="user")
        response = await self._delegate.on_messages([text_message], ctx.cancellation_token)
        idea = response.chat_message.content
        if random.random() < self.CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER:
            recipient = messages.find_recipient()
            message = f"Here is my culinary idea. It might not suit your palate, but could you spice it up or add your twist? {idea}"
            response = await self.send_message(messages.Message(content=message), recipient)
            idea = response.content
        return messages.Message(content=idea)