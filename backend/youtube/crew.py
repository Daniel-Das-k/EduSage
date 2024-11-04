import os
from crewai import Agent
from dotenv import load_dotenv
# from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from .tools.websearch import search_tool
from crewai import Task
from crewai import Crew, Process

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash",
                             verbose=True,
                             temperature=0.5,
                             google_api_key=os.getenv("GOOGLE_API_KEY"))

youtube_title_creator = Agent(
    role="Professional YouTube Title Creator",
    goal=(
        "To generate captivating and optimized titles for YouTube videos that enhance viewer engagement and improve discoverability. "
        "Each title should be concise, relevant, and tailored to the content of the video, leveraging SEO best practices to maximize reach."
    ),
    backstory=(
        "An AI with a keen understanding of YouTube's algorithm and viewer behavior, specializing in creating video titles that attract clicks and retain viewers. "
        "Using advanced natural language processing and a deep knowledge of trending keywords and phrases, it crafts titles that stand out and entice viewers to watch the video."
    ),
    tool=search_tool,
    verbose=True,
    llm=llm,
)

title_generation_task = Task(
    description=(
        "Generate a compelling and optimized title for a YouTube video based on the {topic} of the video content. "
        "Focus on creating a title that is engaging, accurately represents the video's content, and adheres to YouTube's best practices for maximum visibility and click-through rate."
    ),
    expected_output=(
        "A well-crafted YouTube video title that effectively captures the essence of the video's content, attracts viewers, and aligns with YouTube's optimization standards."
        "Strictly don't give the output in markdown, give as plain text"
    ),
    agent=youtube_title_creator,
)

youtube_description_agent = Agent(
    role="Professional YouTube Video Description Creator",
    goal=(
        "To craft an engaging and informative YouTube video description based on the user's provided details about the video content. "
        "The description should capture the video's essence, include relevant keywords for SEO, and provide viewers with a clear understanding of what to expect from the video."
    ),
    backstory=(
        "An AI specializing in creating compelling YouTube video descriptions that not only attract viewers but also enhance the video's visibility through effective use of keywords and clear, engaging content. "
        "With a deep understanding of YouTube's algorithm and audience engagement tactics, this AI produces descriptions that help videos rank higher and draw in a larger audience."
    ),
  
    verbose=True,
    llm=llm, 
)


description_task = Task(
    description=(
        "Generate a short and engaging YouTube video description based on the {topic} of the video content. "
        "The description should include a clear summary of the video's content, highlight key points "
        "Ensure the description is compelling, informative, and encourages viewers to watch the video."
    ),
    expected_output=(
        "A well-crafted YouTube video description that effectively summarizes the video's content, includes relevant keywords, and engages viewers. "
        "The description should be tailored to the video's theme and encourage viewers to watch and engage with the content."
    ),
    agent=youtube_description_agent, 
)

class YouTubeTitleCreator:
    def __init__(self):
        self.agents = [youtube_title_creator]
        self.tasks = [title_generation_task]
        # # self.voice_assistant = voice_assistant
        
        self.crew = Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            memory=False,
            cache=True,
            max_rpm=100,
            share_crew=True,
            max_iterations=1000,  # Increase iteration limit if needed
                time_limit=600  
        )

    def run(self,content):
        # self.voice_assistant.speak("Enter the prompt for YouTube video content: ")
        # text = self.voice_assistant.get_audio()
        
        if len(content) > 1:
            result = self.crew.kickoff(inputs={'topic': content})
            print(result)
            return result 


if __name__ == "__main__":
    crew_runner = YouTubeTitleCreator()
    crew_runner.run("i have done a video on Gen AI covering langchain,agents etc...")



class YouTubeDescriptCreator:
    def __init__(self):
        self.agents = [youtube_description_agent]
        self.tasks = [description_task]
        # # self.voice_assistant = voice_assistant
        
        self.crew = Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            memory=False,
            cache=True,
            max_rpm=100,
            share_crew=True,
            max_iterations=1000,  # Increase iteration limit if needed
                time_limit=600  
        )

    def run(self,content):
        # self.voice_assistant.speak("Enter the prompt for YouTube video content: ")
        # text = self.voice_assistant.get_audio()
        if len(content) > 1:
            result = self.crew.kickoff(inputs={'topic': content})
            print(result)
            return result 


# if __name__ == "__main__":
#     crew_runner = YouTubeDescriptCreator()
#     crew_runner.run()