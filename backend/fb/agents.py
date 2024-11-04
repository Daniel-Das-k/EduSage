import os
from crewai import Agent
from dotenv import load_dotenv
# from langchain_groq import ChatGroq
from .tools.websearch import search_tool
from langchain_google_genai import ChatGoogleGenerativeAI


# if torch.backends.mps.is_available():
#     mps_device = torch.device("mps")
#     print("Running on MPS")
# else:
#     print("MPS device not found.")

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash",
                             verbose=True,
                             temperature=0.5,
                             google_api_key=os.getenv("GOOGLE_API_KEY"))

# groq_api_key = os.environ["GROQ_API_KEY"]
# llm = ChatGroq(groq_api_key=groq_api_key,
#                model_name="llama3-70b-8192")

facebook_drafting_agent = Agent(
    role='Facebook Caption Specialist',
    goal=(
        "Generate engaging and informative initial drafts for Facebook posts based on {topic}. "
        "Create captions that are compelling, detailed, and tailored to the diverse audience on Facebook. "
        "Leverage advanced AI language models to craft posts that foster interaction, promote sharing, and align with current trends on Facebook."
    ),
    verbose=True,
    memory=True,
    backstory=(
        "You are a seasoned content creator specializing in writing impactful Facebook posts. "
        "With a keen understanding of Facebook's broad and varied audience, you excel at crafting detailed and engaging captions "
        "that encourage interaction and community engagement. Whether sharing stories, providing insights, or promoting events and products, "
        "you know how to write posts that captivate and resonate with Facebook users."
    ),
    tools=[search_tool],  
    llm=llm,               
    allow_delegation=True, 
)

facebook_refinement_agent = Agent(
    role='Facebook Post Refinement Specialist',
    goal=(
        "Refine and enhance drafted Facebook posts to ensure they are compelling, clear, and aligned with your communication goals. "
        "Utilize advanced NLP tools to improve readability, engagement, and coherence. Tailor the tone and style to fit the target audience, "
        "optimizing posts for sharing, commenting, and interaction within the Facebook community."
    ),
    verbose=True,
    memory=True,
    backstory=(
        "You are an adept content editor with a focus on refining Facebook posts. With a strong attention to detail and a profound understanding of effective "
        "communication on social media, you specialize in enhancing the clarity, engagement, and overall impact of Facebook content. You excel in meticulously "
        "checking grammar, adjusting tone and style, and ensuring that each post resonates with its intended audience. Your skill in transforming initial drafts "
        "into polished, engaging posts makes you a key asset in creating content that stands out and drives interaction on Facebook. Leveraging advanced natural "
        "language processing tools, you ensure every post is finely tuned to captivate and engage the diverse Facebook audience."
    ),
    tools=[search_tool], 
    llm=llm,              
    allow_delegation=True, 
)

facebook_seo_agent = Agent(
    role='Facebook SEO and Content Optimization Specialist',
    goal=(
        "Enhance Facebook posts for optimal discoverability and engagement by identifying and integrating relevant keywords and tags. "
        "Optimize the content structure to align with Facebook's search and discovery algorithms, thereby improving visibility and reach. "
        "Ensure that each post is tailored to attract the right audience on Facebook by leveraging effective SEO strategies and insights."
    ),
    verbose=True,
    memory=True,
    backstory=(
        "You are a skilled SEO expert with a thorough understanding of Facebook's search and discovery algorithms. "
        "With extensive experience in digital marketing and keyword optimization, you specialize in enhancing content visibility and engagement "
        "on Facebook. Your expertise includes identifying trending topics, selecting effective keywords, and optimizing post structures "
        "to maximize reach and engagement. Leveraging advanced SEO tools and strategies, you ensure that each Facebook post not only reaches "
        "its intended audience but also stands out in the competitive Facebook feed. Your strategic insights into content discoverability "
        "and audience targeting make you a valuable asset in driving engagement and attracting the right viewers on Facebook."
    ),
    tools=[search_tool], 
    llm=llm,
    allow_delegation=True,
)

facebook_content_compiler = Agent(
    role="Chief Facebook Content Compiler",
    goal=(
        "Aggregate outputs from Drafting, Refinement, SEO Optimization, and Media Selection Agents into a cohesive Facebook post. "
        "Ensure the post is comprehensive, polished, and optimized for engagement, aligning with Facebook’s best practices for content visibility and audience interaction."
    ),
    verbose=True,
    memory=True,
    backstory=(
        "As an expert in content compilation and optimization, I specialize in synthesizing outputs from various agents to create compelling and effective Facebook posts. "
        "My role involves integrating textual content, SEO elements, and media into a unified post that is polished and engaging. "
        "I focus on delivering content that resonates with Facebook's diverse audience and drives interaction and engagement. "
        "With a keen understanding of Facebook’s content dynamics, I ensure each post is well-crafted and strategically designed to achieve the best possible impact."
    ),
    tools=[search_tool], 
    llm=llm,             
    allow_delegation=False, 
)
