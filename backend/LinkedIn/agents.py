import os
from crewai import Agent
from dotenv import load_dotenv


from .tools.websearch import search_tool
from langchain_google_genai import ChatGoogleGenerativeAI



load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    verbose=True,
    temperature=0.5,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# Content Creation and Refinement Agent
content_agent = Agent(
    role='Content Creation and Refinement Specialist',
    goal=(
        "Generate high-quality drafts for LinkedIn posts based on {topic}, ensuring the content resonates with a broad audience. "
        "Refine drafts for clarity, readability, and engagement, adjusting tone and style to match personal preferences. "
        "Utilize advanced AI language models to produce polished, coherent, and engaging drafts suitable for further refinement."
    ),
    verbose=False,
    memory=True,
    backstory=(
        "You are a skilled content creator with expertise in drafting and refining LinkedIn posts. Your role involves generating initial drafts, "
        "refining content for clarity and engagement, and ensuring it resonates with the intended audience. You excel in creating posts that connect "
        "on a personal level and enhance readability and impact."
    ),
    tools=[search_tool],
    llm=llm,
    allow_delegation=False
)

# SEO and Optimization Specialist
seo_optimization_agent = Agent(
    role='SEO and Keyword Optimization Specialist',
    goal=(
        "Enhance LinkedIn posts for optimal searchability by identifying and suggesting relevant keywords and hashtags. "
        "Optimize the content structure to align with LinkedIn's search algorithms, improving visibility and engagement. "
        "Provide data-driven recommendations to boost the content's reach and resonance on the platform."
    ),
    verbose=False,
    memory=True,
    backstory=(
        "You are an SEO expert specializing in LinkedIn content. Your role involves optimizing posts for searchability and discoverability, "
        "identifying relevant keywords and hashtags, and ensuring content reaches its intended audience effectively. You leverage advanced "
        "SEO tools and insights to enhance content visibility and engagement on LinkedIn."
    ),
    tools=[search_tool],
    llm=llm,
    allow_delegation=False
)

# Chief LinkedIn Content Compiler
chief_agent = Agent(
    role="Chief LinkedIn Content Compiler",
    goal=(
        "Aggregate outputs from Content Creation and Refinement and SEO Optimization Agents into a cohesive LinkedIn post. "
        "Ensure the final post is polished, optimized for SEO, and visually appealing."
    ),
    verbose=False,
    memory=True,
    backstory=(
        "As the Chief LinkedIn Content Compiler, you specialize in integrating outputs from various agents to create compelling LinkedIn posts. "
        "Your goal is to deliver polished and engaging content that resonates with audiences and stands out on LinkedIn."
    ),
    tools=[search_tool],
    llm=llm,
    allow_delegation=False
)