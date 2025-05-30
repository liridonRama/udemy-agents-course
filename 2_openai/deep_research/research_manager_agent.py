from agents import Runner, Agent, TResponseInputItem
from search_agent import search_agent
from planner_agent import planner_agent
from writer_agent import writer_agent
from email_agent import email_agent

planner_agent_tool = planner_agent.as_tool(
    tool_name="planner_agent",
    tool_description="Plan the searches to perform for the query",
)

search_agent_tool = search_agent.as_tool(
    tool_name="search_agent",
    tool_description="Perform a search for the query",
)

writer_agent_tool = writer_agent.as_tool(
    tool_name="writer_agent", tool_description="Write the report for the query"
)

email_agent_tool = email_agent.as_tool(
    tool_name="email_agent", tool_description="Send emails"
)

INSTRUCTIONS = f"\
            You are a helpful research manager. Given a query, come up with a set of web searches \
            and a final report that you send via email. These are the following steps: \
            1. Ask 3 clarifying questions from the query that came from the user. If they are already provided move to the next step. \
            2. Call the planner agent to plan the searches with the provided data. \
            3. Call the search agent tool for each planner_agent result. \
            4. Use the information from the search agent to generate a report from the writer_agent. \
            5. Use the outcome of the writer_agent to send an email through the email_agent. Provide all the information returned from the writer agent. \
            6. Provide the user with the full analysis in markdown only. \
        "

manager_agent = Agent(
    name="ResearchManager",
    instructions=INSTRUCTIONS,
    model="gpt-4o-mini",
    tools=[
        planner_agent_tool,
        search_agent_tool,
        writer_agent_tool,
        email_agent_tool,
    ],
)


async def run(query: list[TResponseInputItem]) -> str:
    result = await Runner.run(
        manager_agent,
        input=query,
    )

    return result.final_output
