from crewai import Crew, Process

from agents import (
   discord_content_compiler_formatter,
   discord_content_creation_specialist
)
from tasks import (
    content_creation_task_discord,
    compile_and_format_task_discord
)

class Discord:
    def __init__(self):
        # self.voice_assistant = voice_assistant
        self.crew = Crew(
            agents=[
                discord_content_compiler_formatter,
                discord_content_creation_specialist
            ],
            tasks=[
                compile_and_format_task_discord,
                content_creation_task_discord
            ],
            process=Process.sequential,
            memory=False,
            cache=True,
            max_rpm=100,
            share_crew=True
        )

    def run(self,content):
        # self.voice_assistant.speak("Please provide the topic: ")
        # topic = input("Please provide the topic: ")
        # topic = self.voice_assistant.get_audio()
        # self.voice_assistant.speak("Please provide the YouTube link: ")
        # youtube_link = self.voice_assistant.get_audio()
        # youtube_link = input("Please provide the YouTube link: ")

        if len(content) > 1 :
            result = self.crew.kickoff(inputs={'topic': content})
            return result
