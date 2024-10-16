import os
import json
import base64
import hashlib
import re
from flask import Flask, render_template, request, session, redirect, jsonify, send_from_directory
from requests_oauthlib import OAuth2Session
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv
import requests
import facebook
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run_flow
import httplib2
from twitter.crew import Twitter
from summarizer.ytsum import YouTubeTranscriptSummarizer
from LinkedIn.crew import CrewLinkedIn
from transformers import pipeline
from fb.crew import Facebook
from langchain_community.agent_toolkits import GmailToolkit
from langchain import hub
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_openai import ChatOpenAI
from langchain.load import dumps, loads
from langchain_core.messages import AIMessage, HumanMessage
from youtube.crew import YouTubeTitleCreator, YouTubeDescriptCreator
import random
import time
from zenora import APIClient
from discord.creds import TOKEN, CLIENT_SECRET, REDIRECT_URI, OAUTH_URL

load_dotenv()
pipe = pipeline("text-classification", model="Varun53/openai-roberta-large-AI-detection")
app = Flask(__name__)
CORS(app)
app.config["SECRET_KEY"] = os.urandom(24)
fb = Facebook()

# Database and file upload configurations
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

db = SQLAlchemy(app)

# Ensure upload folder and output directories exist
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])
if not os.path.exists('outputs/ytVideoSummarizer'):
    os.makedirs('outputs/ytVideoSummarizer')

# Twitter OAuth configuration
client_id = os.getenv("TWITTER_OAUTH_CLIENT_ID")
client_secret = os.getenv("TWITTER_OAUTH_CLIENT_SECRET")
redirect_uri = "http://127.0.0.1:5000/oauth/callback"
auth_url = "https://twitter.com/i/oauth2/authorize"
token_url = "https://api.twitter.com/2/oauth2/token"
scopes = ["tweet.read", "users.read", "tweet.write", "offline.access"]

#linkedin
linkedin_client_id = os.getenv('LINKEDIN_CLIENT_ID')
linkedin_client_secret = os.getenv('LINKEDIN_CLIENT_SECRET')
linkedin_redirect_uri = os.getenv('LINKEDIN_REDIRECT_URI')


CLIENT_SECRETS_FILE = "youtube_creds.json"
YOUTUBE_UPLOAD_SCOPE = "https://www.googleapis.com/auth/youtube.upload"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0
To make this sample run you will need to populate the client_secrets.json file
found at:
   %s
with information from the API Console
https://console.cloud.google.com/
For more information about the client_secrets.json file format, please visit:
https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
""" % os.path.abspath(os.path.join(os.path.dirname(__file__), CLIENT_SECRETS_FILE))

class YouTubeUploader:
    def init(self):
        self.title = None
        self.description = None

    def set_content(self, title, description):
        self.title = title
        self.description = description

    def get_authenticated_service(self):
        flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE, scope=YOUTUBE_UPLOAD_SCOPE, message=MISSING_CLIENT_SECRETS_MESSAGE)
        storage = Storage("youtube-oauth2.json")
        credentials = storage.get()
        if credentials is None or credentials.invalid:
            credentials = run_flow(flow, storage)
        return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, http=credentials.authorize(httplib2.Http()))

    def initialize_upload(self, youtube, video_file):
        body = dict(
            snippet=dict(
                title=self.title,
                description=self.description,
                categoryId="22"
            ),
            status=dict(
                privacyStatus="public"
            )
        )
        insert_request = youtube.videos().insert(
            part=",".join(body.keys()),
            body=body,
            media_body=MediaFileUpload(video_file, chunksize=-1, resumable=True)
        )
        self.resumable_upload(insert_request)

    def resumable_upload(self, insert_request):
        response = None
        error = None
        retry = 0
        while response is None:
            try:
                status, response = insert_request.next_chunk()
                if response is not None:
                    if 'id' in response:
                        print("Video id was successfully uploaded: %s" % response['id'])
                    else:
                        exit("The upload failed with an unexpected response: %s" % response)
            except HttpError as e:
                if e.resp.status in [500, 502, 503, 504]:
                    error = "A retriable HTTP error %d occurred:\n%s" % (e.resp.status, e.content)
                else:
                    raise
            except Exception as e:
                error = "An exception occurred: %s" % e

            if error is not None:
                print(error)
                retry += 1
                if retry > 10:
                    exit("No longer attempting to retry.")
                max_sleep = 2 ** retry
                sleep_seconds = random.random() * max_sleep
                print("Sleeping %f seconds and then retrying..." % sleep_seconds)
                time.sleep(sleep_seconds)

    def upload(self, video_file):
        if not os.path.exists(video_file):
            return "Invalid file path"
        youtube_service = self.get_authenticated_service()
        try:
            self.initialize_upload(youtube_service, video_file)
            return "Upload successful"
        except HttpError as e:
            return "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)

class PostLinkedIn:
    def init(self):
        self.access_token = None

    def set_access_token(self, access_token):
        self.access_token = access_token

    def create_post(self, content):
        if not self.access_token:
            raise ValueError("Access token is not set.")
        with open('linkedin_token.json', 'r') as f:
            l_tokens = json.load(f)
        url = 'https://api.linkedin.com/v2/ugcPosts'
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        payload = {
            "author": f"urn:li:person:{l_tokens['id']}",
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    
                        "shareCommentary": {
                            "text": content
                        },
                        "shareMediaCategory": "NONE"
                    
                    
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
            }
        }
        response = requests.post(url, headers=headers, json=payload)
        print("text response",response)
        if response.status_code != 201:
            print(f"Failed to create post: {response.json()}")
        return response.json()

    def create_post_with_image(self, content, image_urn):
        if not self.access_token:
            raise ValueError("Access token is not set.")
        with open('linkedin_token.json', 'r') as f:
            l_tokens = json.load(f)
        

        url = 'https://api.linkedin.com/v2/ugcPosts'
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        payload = {
            "author": f"urn:li:person:{l_tokens['id']}",
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                   
                        "shareCommentary": {
                            "text": content
                        },
                        "shareMediaCategory": "IMAGE",
                        "media": [
                            {
                                "status": "READY",
                                "description": {
                                    "text": "Image description"
                                },
                                "media": image_urn,
                                "title": {
                                    "text": "Image Title"
                                }
                            }
                        ]
                    
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
            }
        }
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code != 201:
            print(f"Failed to create post with image: {response.json()}")
        return response.json()


class LinkedinManager:
    def init(self):
        self.access_token = None
        self.user_id = None
        self.load_tokens()

    def load_tokens(self):
        try:
            with open("linkedin_token.json", 'r') as f:
                token = json.load(f)
                self.access_token = token.get("access_token")
                self.user_id = token.get("id")

            if not self.access_token or not self.user_id:
                raise ValueError("LinkedIn token or ID is missing in linkedin_token.json")

        except FileNotFoundError:
            print("linkedin_token.json file not found.")
        except ValueError as ve:
            print(f"Error: {ve}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def upload_image_to_linkedin(self,access_token:str, user_id:str, image_path):
        """Upload an image to LinkedIn and return the upload reference."""
        # Initialize the upload
        init_url = "https://api.linkedin.com/v2/assets?action=registerUpload"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        upload_request_body = {
            "registerUploadRequest": {
                "recipes": ["urn:li:digitalmediaRecipe:feedshare-image"],
                "owner": f"urn:li:person:{user_id}",
                "serviceRelationships": [
                    {
                        "relationshipType": "OWNER",
                        "identifier": "urn:li:userGeneratedContent"
                    }
                ]
            }
        }

        response = requests.post(init_url, headers=headers, json=upload_request_body)
        response.raise_for_status()

        upload_info = response.json()
        upload_url = upload_info['value']['uploadMechanism']['com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest']['uploadUrl']
        asset = upload_info['value']['asset']

        # Upload the image
        with open(image_path, 'rb') as image_file:
            image_headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/octet-stream"
            }
            image_response = requests.put(upload_url, headers=image_headers, data=image_file)
            image_response.raise_for_status()

            return asset

    def post_to_linkedin(self, content, image_path=None):
        # if not self.access_token:
        #     raise ValueError("Access token is not available. Please log in to LinkedIn first.")
        with open("linkedin_token.json", 'r') as f:
                token = json.load(f)
                self.access_token = token.get("access_token")
                self.user_id = token.get("id")
        linkedin = PostLinkedIn()
        linkedin.set_access_token(self.access_token)

        if image_path:
            image_urn = self.upload_image_to_linkedin(self.access_token,self.user_id,image_path)
            response = linkedin.create_post_with_image(content, image_urn)
        else:
            response = linkedin.create_post(content)
        return response

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    photo = db.Column(db.String(200), nullable=True)



if __name__ == '__main__':
        port = int(os.environ.get("PORT", 5000))
        app.run(host='0.0.0.0', port=port)