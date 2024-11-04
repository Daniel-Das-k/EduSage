from crewai import Crew, Process
from .agents import content_agent, seo_optimization_agent, chief_agent
from .tasks import chief_agent, seo_task, chief_task, content_task

class CrewLinkedIn:
    def __init__(self):
        self.agents = [content_agent,seo_optimization_agent,chief_agent]
        self.tasks = [content_task,seo_task,chief_task]
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

    def run(self,content):
        # self.voice_assistant.speak("Enter the Topic to be posted on : ")
        # text = self.voice_assistant.get_audio()
        # text = input("Enter: ")
        if len(content) > 1:
            result = self.crew.kickoff(inputs={'topic': content})
            print(result)
            return result



    