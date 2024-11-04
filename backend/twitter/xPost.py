# import json
# import requests
# from crew import Twitter

# class TwitterPoster:
#     def __init__(self, token_file='twitter_access.json'):
#         self.token_file = token_file

#     def get_access_token(self):
#         with open(self.token_file, 'r') as f:
#             token_data = json.load(f)
#             return token_data['access_token']

#     def post_tweet(self):
#         access_token = self.get_access_token()
#         xcrew = Twitter()
#         text = input("Enter:")
#         post = xcrew.run(text)

#         # Print the type and content of the post for debugging
#         print(f"Type of post: {type(post)}")
#         print(f"Content of post: {post}")

#         # Ensure post is JSON-serializable
#         if hasattr(post, 'to_dict'):
#             post = post.to_dict()

#         # If post is a dict, extract the relevant text
#         if isinstance(post, dict):
#             payload = {
#                 "text": post.get('content', 'Default tweet text')
#             }
#         else:
#             # Ensure post is a string
#             payload = {"text": str(post)}

#         response = self.post_tweet_api(payload, access_token)
#         return response

#     def post_tweet_api(self, payload, token):
#         print("Tweeting!")
#         response = requests.post(
#             "https://api.twitter.com/2/tweets",
#             json=payload,
#             headers={
#                 "Authorization": f"Bearer {token}",
#                 "Content-Type": "application/json",
#             },
#         )
#         print("Posted:", payload["text"])
#         return response

# class CrewOutput:
#     def __init__(self, content):
#         self.content = content

#     def to_dict(self):
#         return {
#             "content": self.content
#         }

# if __name__ == "__main__":
#     xpost = TwitterPoster()
#     xpost.post_tweet()
import json
from crew import Twitter
import requests

class TwitterPoster:
    def __init__(self, token_file='twitter_access.json'):
        self.token_file = token_file

    def get_access_token(self):
        with open(self.token_file, 'r') as f:
            token_data = json.load(f)
            return token_data['access_token']

    def post_tweet(self):
        access_token = self.get_access_token()
        xcrew = Twitter()
        text = input(": ")
        post=xcrew.run(text)
        payload = {
            "text": str(post)
        }
        response = self.post_tweet_api(payload, access_token)
        return response

    def post_tweet_api(self, payload, token):
        print("Tweeting!")
        response = requests.post(
            "https://api.twitter.com/2/tweets",
            json=payload,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            },
        )
        print("Posted:", payload["text"])
        return response

if __name__ == "__main__":
    xpost = TwitterPoster()
    # xcrew = Twitter()
    # xtweet = xcrew.run()
    
    xpost.post_tweet()