
from crewai_tools import tool
import os, requests, re
# from crewai_tools.tools import FileReadTool

@tool
def generateimage(details: str) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    response = client.images.generate(
        model="dall-e-3",
        prompt = (f"Create a professional and engaging image for a LinkedIn post about {details}. The image should be clean, modern, and visually appealing, using a color scheme that complements LinkedIn's branding (blues, grays, and whites). Focus on clarity and simplicity, avoiding clutter and excessive detail. Incorporate relevant icons, graphics, or abstract visuals that enhance the post's message and attract the audience's attention. Ensure the image aligns with the professional tone and aesthetic of LinkedIn, and avoid any text or overt promotional elements within the image itself. The composition should be balanced and draw the viewer's eye naturally towards the key visual elements that support the post's content. DO NOT include any text within the image. DO NOT use bright or flashy colors that detract from the professional feel. """
),
        size="1024x1024",
        quality="standard",
        n=1,
    )
    image_url = response.data[0].url
    words = details.split()[:5] 
    safe_words = [re.sub(r'[^a-zA-Z0-9_]', '', word) for word in words]  
    filename = "_".join(safe_words).lower() + ".png"
    filepath = os.path.join(os.getcwd(), filename)

    # Download the image from the URL
    image_response = requests.get(image_url)
    if image_response.status_code == 200:
        with open(filepath, 'wb') as file:
            file.write(image_response.content)
    else:
        print("Failed to download the image.")
        return ""

    return filepath

# file_read_tool = FileReadTool(
# 	file_path='template.md',
# 	description='A tool to read the Story Template file and understand the expected output format.'
# )
