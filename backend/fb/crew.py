from crewai import Crew, Process
from .agents import (
    facebook_content_compiler,
    facebook_drafting_agent,
    facebook_refinement_agent,
    facebook_seo_agent
)
from .tasks import (
    drafting_task_facebook,
    editing_task_facebook,
    seo_task_facebook,
    chief_task_facebook,
  
)

class Facebook:
    def __init__(self):
        # self.voice_assistant = voice_assistant
        self.crew = Crew(
            agents=[facebook_drafting_agent,facebook_refinement_agent,facebook_seo_agent,facebook_content_compiler],
            tasks=[drafting_task_facebook,editing_task_facebook,seo_task_facebook,chief_task_facebook],
            process=Process.sequential,
            memory=False,
            cache=True,
            max_rpm=100,
            share_crew=True
        )

    def run(self,content):
        # self.voice_assistant.speak("Topic: ")
        # text = self.voice_assistant.get_audio()
        # text = input(": ")
        if len(content) > 1:
            result = self.crew.kickoff(inputs={'topic': content})
            print(result)
            return result
        

# if __name__ == "__main__":
#     generator = Facebook()

#     text = input("Enter the topic for the Facebook post: ")

#     result = generator.run(topic=text)
#     print(result)