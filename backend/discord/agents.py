import os
from crewai import Agent
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from tools.search_tools import search_tool


load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash",
                             verbose=True,
                             temperature=0.5,
                             google_api_key=os.getenv("GOOGLE_API_KEY"))

discord_content_creation_specialist = Agent(
    role='Discord Content Creation Specialist',
    goal="Generate, refine, and optimize Discord messages for clarity, engagement, and discoverability.",
    verbose=False,
    memory=True,
    backstory="Specializes in creating, refining, and optimizing Discord messages tailored to the community's interests and communication style.",
    tools=[search_tool], 
    llm=llm,
    allow_delegation=False,
)

discord_content_compiler_formatter = Agent(
    role="Chief Discord Content Compiler and Formatter",
    goal="Aggregate, format, and optimize content for Discord posts, ensuring they are cohesive, and aligned with Discord's best practices.",
    verbose=False,
    memory=True,
    backstory="Specializes in synthesizing various content elements into unified and engaging posts that enhance readability and engagement on Discord.",
    tools=[search_tool],  
    llm=llm,
    allow_delegation=False,
)