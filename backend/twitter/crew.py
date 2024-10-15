import os
import json
from dotenv import load_dotenv
load_dotenv()
import re
from crewai import  Crew
from crewai.process import Process
from .tasks import topic_analysis_and_research,create_twitter_posts
from .agents import trending_topic_and_content_researcher_agent,creative_content_creator_agent

class Twitter:
	def __init__(self):
		# self.voice_assistant = voice_assistant
		self.crew = Crew(
			agents=[trending_topic_and_content_researcher_agent,creative_content_creator_agent],
			tasks=[topic_analysis_and_research,create_twitter_posts],
			process=Process.sequential,
			memory=False,
            cache=True,
            max_rpm=100,
            share_crew=True
		)

	def run(self,content):
		# self.voice_assistant.speak("Say the topic to tweet about: ")
		# text = self.voice_assistant.get_audio()
		# text = input("Enter the topic to tweet about: : ")
		if len(content) > 1:
			result = self.crew.kickoff(inputs={'topic': content})
			print(result)
			return result
   

