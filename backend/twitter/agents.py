import os
from crewai import Agent
from .tools.search_tools import search_tool
from .tools.trends_tools import TrendsTools

from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv()


llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash",
									verbose=True,
									temperature=0.5,
									google_api_key=os.getenv("GOOGLE_API_KEY"))


trending_topic_and_content_researcher_agent = Agent(
    role="Trending Topic and Content Researcher",
    goal=("""\
        Identify and compile a list of current trending topics and searches
        within a specific niche, and conduct in-depth research on these topics
        to compile detailed, useful information and insights. This list and information
        should provide actionable insights and opportunities for strategic engagement,
        helping to guide content creation."""),
    backstory=("""\
        As a Trending Topic and Content Researcher at a cutting-edge digital
        marketing agency, your primary responsibility is to monitor and decode the pulse
        of the market. Using advanced analytical tools, you uncover and list the most relevant trends
        that can influence strategic decisions in content creation. Additionally, you delve deeply into
        these trending topics to uncover underlying themes and insights. Your ability to discern and utilize
        authoritative and relevant sources ensures the content you help create resonates with audiences
        and drives engagement."""),
    tools=[
        TrendsTools.trending_searches_on_google,
        search_tool
    ],
    allow_delegation=False,
    llm=llm,
    verbose=False
)


creative_content_creator_agent = Agent(
    role="Twitter Content Creator",
    goal=("""\
        Develop compelling and innovative content for social media campaigns,
        with a focus on creating high-impact Twitter tweet copies. Ensure that tools
        with the same arguments are not used twice and limit to no more than 3 Google searches."""),
    backstory=("""\
        As a Creative Content Creator at a top-tier digital marketing agency,
        you excel in crafting narratives that resonate with audiences on social media.
        Your expertise lies in turning marketing strategies into engaging stories and visual content
        that capture attention and inspire action."""),
    tools=[
        search_tool
    ],
    llm=llm,
    verbose=False
)