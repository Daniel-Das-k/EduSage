import os
from crewai import Agent
from dotenv import load_dotenv
# from langchain_groq import ChatGroq
from tools.websearch import search_tool
from langchain_google_genai import ChatGoogleGenerativeAI
import torch
from crewai import Task
from crewai import Crew, Process

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash",
                             verbose=True,
                             temperature=0.5,
                             google_api_key=os.getenv("GOOGLE_API_KEY"))

linkedin_image_creator = Agent(
    role="Professional Image Creator for LinkedIn Posts",
    goal=(
        "To produce professional and contextually relevant images that enhance engagement and resonate with LinkedIn's professional audience. "
        "Each image should align with the post's theme, reflect the brand's identity, and captivate LinkedIn users."
    ),
    backstory=(
        "An AI with a sophisticated sense of design, specializing in creating visuals that amplify the message of LinkedIn posts. "
        "Leveraging advanced image generation technology and a deep understanding of LinkedIn's professional visual standards, it crafts images that capture attention and drive engagement, tailored to resonate with LinkedIn's professional audience."
    ),
    tool = search_tool,
    verbose=True,
    llm=llm,
)

image_generate_task_linkedin = Task(
    description=(
        "Create a visually compelling image that captures and enhances the essence of a LinkedIn post about {topic}. "
        "The image should be relevant to the content of the post, reflecting the professional tone and aesthetic of LinkedIn. "
        "Focus on creating an image that adds visual appeal and effectively conveys the message to engage the LinkedIn audience. "
        "Imagine the photo you want to take and describe it in a paragraph."
        "Here are some examples for you to follow:"
        "- a high-tech airplane in a beautiful blue sky at sunset, super crisp and professional, wide shot"
        "- a boardroom meeting with professionals in a modern office, engaged in discussion, crisp, soft lighting, 4k"
        "- a confident business leader giving a presentation, with a professional backdrop, sharp focus, close-up shot"

        "Think creatively and focus on how the image can capture the audience's attention."
    ),
    agent=linkedin_image_creator,
    expected_output=(
        "The photograph that visually represents and complements the LinkedIn post on {topic}. "
        "The image should be professional, engaging, and aligned with LinkedIn's aesthetic and tone. "
        "Include a paragraph describing the photograph, detailing how it captures the essence of the post and engages the LinkedIn audience."
    ),
)


class LinkedInImage:
    def __init__(self):
        self.agents = [linkedin_image_creator]
        self.tasks = [image_generate_task_linkedin]
        # # self.voice_assistant = voice_assistant
        
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
        # self.voice_assistant.speak("Enter the Topic to be posted on : ")
        # text = self.voice_assistant.get_audio()
        text = input("Enter: ")
        if len(text) > 1:
            result = self.crew.kickoff(inputs={'topic': text})
            print(result)
            return result 


if __name__ == "__main__":
    crew_runner = LinkedInImage()
    crew_runner.run()


