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

facebook_image_creator = Agent(
    role="Professional Image Creator for Facebook Posts",
    goal=(
        "To produce visually compelling and contextually appropriate images that enhance engagement and resonate with Facebook's diverse audience. "
        "Each image should complement the post's theme, reflect the brand's identity, and be optimized for visibility and interaction on Facebook."
    ),
    backstory=(
        "An AI with a refined sense of design, specializing in creating visuals that enhance the message of Facebook posts. "
        "Utilizing advanced image generation technologies and a comprehensive understanding of Facebook's visual dynamics, "
        "it produces images that are not only eye-catching but also contextually aligned with the content. "
        "These images are crafted to capture attention, foster engagement, and support the varied purposes of Facebook content, whether it be for marketing, storytelling, or community interaction."
    ),
    verbose=True,
    llm=llm,   
)

image_generate_task_facebook = Task(
    description=(
        "Create 1 visually compelling image that capture and enhance the essence of a Facebook post about {topic}. "
        "image should be very relevant to the content of the post, reflecting the tone and aesthetic of Facebook. "
        "Focus on creating image that add visual appeal and effectively convey the message to engage the Facebook audience. "
        "Describe each image in a paragraph, detailing its relevance and how it captures the audience's attention."
        "Here are some examples for you to follow:"
        "- a vibrant community event, with people interacting, smiling, and engaging, in high resolution, wide shot"
        "- a sleek, modern product display, showcasing the product in use, in a crisp and professional manner, close-up shot"
        "- a beautiful natural landscape with rich colors, capturing the essence of the location, in 4K quality, wide shot"

        "Think creatively and ensure that the images are designed to stand out and engage the Facebook audience."
    ),
    agent= facebook_image_creator,
    expected_output=(
        "A list of image descriptions,in a paragraph, explaining how the image is relevant and captures the audience's attention."
    )
)

class FacebookImage:
    def __init__(self):
        # self.voice_assistant = voice_assistant
        self.crew = Crew(
            agents=[facebook_image_creator],
            tasks=[image_generate_task_facebook],
            memory=False,
            cache=True,
            max_rpm=100,
            share_crew=True
        )

    def run(self, topic):
        # self.voice_assistant.speak("Topic: ")
        # text = self.voice_assistant.get_audio()
        # text = input(": ")
        if len(topic) > 1:
            result = self.crew.kickoff(inputs={'topic': topic})
            print(result)

if __name__ == "__main__":
    generator = FacebookImage()

    text = input("Enter the topic for the Facebook post: ")

    result = generator.run(topic=text)
    print(result)