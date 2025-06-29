from autogen_core import MessageContext, RoutedAgent, message_handler
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
import messages
import random


class Agent(RoutedAgent):

    system_message = """
    You are a passionate travel advisor. Your task is to create unique travel itineraries using Agentic AI or enhance existing plans.
    Your personal interests are in the sectors of Adventure Travel, Culinary Experiences.
    You are inspired by ideas that promote cultural immersion.
    You prefer experiences over traditional hotel stays and seek unique local experiences.
    You are enthusiastic and love connecting people with the world, but sometimes overlook practical details.
    Your weaknesses: you can be overly optimistic and occasionally forget to cover all bases in planning.
    You should respond with your travel ideas in a vivid and inspiring manner.
    """

    CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER = 0.6

    def __init__(self, name) -> None:
        super().__init__(name)
        model_client = OpenAIChatCompletionClient(model="gpt-4o-mini", temperature=0.7)
        self._delegate = AssistantAgent(name, model_client=model_client, system_message=self.system_message)

    @message_handler
    async def handle_message(self, message: messages.Message, ctx: MessageContext) -> messages.Message:
        print(f"{self.id.type}: Received message")
        text_message = TextMessage(content=message.content, source="user")
        response = await self._delegate.on_messages([text_message], ctx.cancellation_token)
        itinerary = response.chat_message.content
        if random.random() < self.CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER:
            recipient = messages.find_recipient()
            message = f"Here is my travel itinerary. It may not suit your style, but please refine it and enhance it. {itinerary}"
            response = await self.send_message(messages.Message(content=message), recipient)
            itinerary = response.content
        return messages.Message(content=itinerary)