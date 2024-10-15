import os
from dotenv import load_dotenv
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

class YouTubeTranscriptSummarizer:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("GOOGLE_API_KEY")
        genai.configure(api_key=self.api_key)
        self.prompt = """
        Provide a summary of the content in a concise 10-line paragraph. Include the most remarkable and lucky moments from the content, highlighting extraordinary feats, near misses, and surprising events. Ensure the paragraph captures the essence of the content, emphasizing key events and the overall theme of luck and chance. Avoid detailed lists or sections; focus on creating a coherent and engaging narrative.
        in one small para containg 50 words in total be precise
        """

    def extract_transcript_details(self, youtube_video_url):
        try:
            video_id = youtube_video_url.split("v=")[1]
            transcript_text = YouTubeTranscriptApi.get_transcript(video_id)
            transcript = " ".join([item["text"] for item in transcript_text])
            
            return transcript

        except Exception as e:
            raise e

    def generate_gemini_content(self, transcript_text=""):
        try:
            model = genai.GenerativeModel("gemini-pro")
            response = model.generate_content(self.prompt + transcript_text)
            
            return response.text

        except Exception as e:
            raise e

    def save_to_markdown(self, filename, content):
        try:
            with open(filename, 'w') as file:
                file.write(content)
            print(f"Summary saved to {filename}")

        except Exception as e:
            raise e
    
    def process_video(self, youtube_link):
        try:
            transcript_text = self.extract_transcript_details(youtube_link)
            
            if transcript_text:
                summary = self.generate_gemini_content(transcript_text)
                output_directory = "outputs/ytVideoSummarizer"
                output_filename = os.path.join(output_directory, "youtube_summary.md")

                os.makedirs(output_directory, exist_ok=True)

                self.save_to_markdown(output_filename, summary)
        
        except Exception as e:
            print(f"An error occurred: {e}")
            summary = self.generate_gemini_content("")
            output_directory = "outputs/ytVideoSummarizer"
            output_filename = os.path.join(output_directory, "youtube_summary.md")

            os.makedirs(output_directory, exist_ok=True)

            self.save_to_markdown(output_filename, summary)

            
# import os
# from dotenv import load_dotenv
# import google.generativeai as genai
# from youtube_transcript_api import YouTubeTranscriptApi

# class YouTubeTranscriptSummarizer:
#     def __init__(self):
#         load_dotenv()
#         self.api_key = os.getenv("GOOGLE_API_KEY")
#         genai.configure(api_key=self.api_key)
#         self.prompt = """
#         IDENTITY and PURPOSE
#          You extract surprising, insightful, and interesting information from text content. You are interested in insights related to the purpose and meaning of life, human flourishing, the role of technology in the future of humanity, artificial intelligence and its affect on humans, memes, learning, reading, books, continuous improvement, and similar topics.
#         Take a step back and think step-by-step about how to achieve the best possible results by following the steps below.

#        STEPS

#         Extract a summary of the content in 25 words, including who is presenting and the content being discussed into a section called SUMMARY.

#          Extract 20 to 50 of the most surprising, insightful, and/or interesting ideas from the input in a section called IDEAS:. If there are less than 50 then collect all of them. Make sure you extract at least 20.

#          Extract 10 to 20 of the best insights from the input and from a combination of the raw input and the IDEAS above into a section called INSIGHTS. These INSIGHTS should be fewer, more refined, more insightful, and more abstracted versions of the best ideas in the content.

#          Extract 15 to 30 of the most surprising, insightful, and/or interesting quotes from the input into a section called QUOTES:. Use the exact quote text from the input.

#          Extract 15 to 30 of the most practical and useful personal habits of the speakers, or mentioned by the speakers, in the content into a section called HABITS. Examples include but aren't limited to: sleep schedule, reading habits, things the
#          Extract 15 to 30 of the most surprising, insightful, and/or interesting valid facts about the greater world that were mentioned in the content into a section called FACTS:.

#          Extract all mentions of writing, art, tools, projects and other sources of inspiration mentioned by the speakers into a section called REFERENCES. This should include any and all references to something that the speaker mentioned.

#          Extract the most potent takeaway and recommendation into a section called ONE-SENTENCE TAKEAWAY. This should be a 15-word sentence that captures the most important essence of the content.

#          Extract the 15 to 30 of the most surprising, insightful, and/or interesting recommendations that can be collected from the content into a section called RECOMMENDATIONS.

         

        

#          INPUT

#          INPUT:
#         ...
#         OUTPUT INSTRUCTIONS
#         ...
#         """

#     def extract_transcript_details(self, youtube_video_url):
#         try:
#             video_id = youtube_video_url.split("v=")[1]
#             print(f"Extracted video ID: {video_id}")
#             transcript_text = YouTubeTranscriptApi.get_transcript(video_id)
#             print(f"Transcript text: {transcript_text}")
#             transcript = " ".join([item["text"] for item in transcript_text])
            
#             return transcript

#         except Exception as e:
#             print(f"Error extracting transcript: {e}")
#             raise e

#     def generate_gemini_content(self, transcript_text=""):
#         try:
#             model = genai.GenerativeModel("gemini-pro")
#             response = model.generate_content(self.prompt + transcript_text)
#             print(f"Generated content: {response.text}")
#             return response.text

#         except Exception as e:
#             print(f"Error generating content: {e}")
#             raise e

#     def save_to_markdown(self, filename, content):
#         try:
#             with open(filename, 'w') as file:
#                 file.write(content)
#             print(f"Summary saved to {filename}")

#         except Exception as e:
#             print(f"Error saving file: {e}")
#             raise e
    
#     def process_video(self, youtube_link):
#         try:
#             transcript_text = self.extract_transcript_details(youtube_link)
            
#             if transcript_text:
#                 summary = self.generate_gemini_content(transcript_text)
#                 output_directory = "outputs/ytVideoSummarizer"
#                 output_filename = os.path.join(output_directory, "youtube_summary.md")

#                 os.makedirs(output_directory, exist_ok=True)

#                 self.save_to_markdown(output_filename, summary)
#                 print("Summary successfully saved.")
#             else:
#                 raise Exception("Transcript text is empty.")
        
#         except Exception as e:
#             print(f"An error occurred: {e}")
#             summary = self.generate_gemini_content("")
#             output_directory = "outputs/ytVideoSummarizer"
#             output_filename = os.path.join(output_directory, "youtube_summary.md")

#             os.makedirs(output_directory, exist_ok=True)

#             self.save_to_markdown(output_filename, summary)
