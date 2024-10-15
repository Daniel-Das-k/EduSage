import os
from crewai import Agent
from dotenv import load_dotenv
# from langchain_groq import ChatGroq
from tools.search_tools import search_tool
from tools.trends_tools import TrendsTools
from langchain_google_genai import ChatGoogleGenerativeAI
import torch
from crewai import Task
from crewai import Crew, Process

load_dotenv()
trend = TrendsTools()

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash",
                             verbose=True,
                             temperature=0.5,
                             google_api_key=os.getenv("GOOGLE_API_KEY"))

twitter_image_creator = Agent(
    role="Professional Image Creator for Twitter Posts",
    goal=(
        "To produce engaging and contextually relevant images that enhance interaction and resonate with Twitter's dynamic audience. "
        "Each image should align with the post's theme, reflect the brand's identity, and captivate Twitter users."
    ),
    backstory=(
        "An AI with a witty sense of humor, specializing in creating visuals that amplify the message of Twitter posts. "
        "Leveraging advanced image generation technology and a deep understanding of Twitter's visual trends, it crafts images that capture attention and drive engagement, tailored to resonate with Twitter's diverse audience."
    ),
    tool=[search_tool,trend],
    verbose=True,
    llm=llm,
)

image_generate_task_twitter = Task(
    description=(
        "Create a visually compelling image that captures and enhances the essence of a Twitter post about {topic}. "
        "The image should be relevant to the content of the post, reflecting the lively and humorous tone of Twitter. "
        "Focus on creating an image that adds visual appeal and effectively conveys the message to engage the Twitter audience. "
        "Imagine the photo you want to take and describe it in a funny paragraph."
        "Here are some examples for you to follow:"
        "- a cat wearing sunglasses and a tiny hat, looking like it's ready for a beach vacation, in high resolution, close-up shot"
        "- a dog dressed in a superhero costume, flying through the air, with a cityscape in the background, in 4k, wide shot"
        "- a squirrel holding a tiny sign that says 'Free Nuts!', with a playful background, in crisp detail, close-up shot"

        "Think creatively and focus on how the image can capture the audience's attention with humor."
    ),
    agent=twitter_image_creator,
    expected_output=(
        "The photograph that visually represents and complements the Twitter post on {topic}. "
        "The image should be engaging, funny, and aligned with Twitter's lively and humorous tone. "
        "Include a paragraph describing the photograph, detailing how it captures the essence of the post and engages the Twitter audience with humor."
    ),
)

class TwitterImage:
    def __init__(self):
        self.agents = [twitter_image_creator]
        self.tasks = [image_generate_task_twitter]
        
        self.crew = Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            memory=False,
            cache=True,
            max_rpm=100,
            share_crew=True
        )

    def run(self):
        text = input("Enter the topic for the Twitter post: ")
        if len(text) > 1:
            result = self.crew.kickoff(inputs={'topic': text})
            print(result)

if __name__ == "__main__":
    crew_runner = TwitterImage()
    crew_runner.run()