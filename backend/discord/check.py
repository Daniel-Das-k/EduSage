import requests
from crew import Discord

# Initialize Discord instance
discord = Discord()
url = "https://discord.com/api/v9/channels/935570425864405034/messages"
headers = {
    "Authorization": "NzYwMTM4NTQyNTIwNzI5NjMw.GjB0yx.ZQ6mlZ6iWCb_adp1Lp61yzSkdXvEjMyo735IY8"
}

def post_text(content_text):
    content = discord.run(content_text)
    print(content)
    payload = {"content": str(content)}
    res = requests.post(url, data=payload, headers=headers)
    print("Posted text:", res.status_code)

def post_image(content_text, image_path):
    content = discord.run(content_text)
    print(content)
    payload = {"content": str(content)}
    with open(image_path, "rb") as image:
        files = {"file": image}
        res = requests.post(url, data=payload, headers=headers, files=files)
    print("Posted image:", res.status_code)

def post_video(content_text, video_path):
    content = discord.run(content_text)
    print(content)
    payload = {"content": str(content)}
    with open(video_path, "rb") as video:
        files = {"file": video}
        res = requests.post(url, data=payload, headers=headers, files=files)
    print("Posted video:", res.status_code)

# Example usage:
# post_text("Team Build Wheels won Hackmaggedon by presenting an innovative automation app. Summarize their achievement and the app's features. Ensure the summary is engaging and clear, highlighting the key aspects and impact of the app. Make sure the content resonates with the audience and maintains a compelling narrative.")
# post_text("Generative ai is something we need to look for in the future")
# post_image("This post is about my greatest Head Of Dept I would love to share this post Mr. Sekar", "image.png")
# post_video("Team Build Wheels won Hackmaggedon by presenting an innovative automation app. Summarize their achievement and the app's features. Ensure the summary is engaging and clear, highlighting the key aspects and impact of the app. Make sure the content resonates with the audience and maintains a compelling narrative.", "bbaf4p.mpg")

# post_image("Dhoni finishes off in style","image.png")