# from dotenv import load_dotenv
# import os
# from crewai_tools import SerperDevTool

# load_dotenv()
# os.environ["SERPER_API_KEY"] = os.getenv("SERPER_API_KEY")

# tool = SerperDevTool()
# query = "best restaurants in New York"


from langchain_community.tools import DuckDuckGoSearchRun

search_tool = DuckDuckGoSearchRun()