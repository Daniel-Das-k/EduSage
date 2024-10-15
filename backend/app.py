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

# VALID_PRIVACY_STATUSES = ("public", "private", "unlisted")
# from langchain_community.tools.gmail.utils import (
#     build_resource_service,
#     get_gmail_credentials,
# )

# os.environ["OPENAI_API_KEY"] ="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"


# credentials = get_gmail_credentials(
#     token_file="token.json",
#     scopes=["https://mail.google.com/"],
#     client_secrets_file="credentials.json",
# )
# api_resource = build_resource_service(credentials=credentials)
# toolkit = GmailToolkit(api_resource=api_resource)
# tools = toolkit.get_tools()

# instructions = """You are an assistant that creates email drafts."""
# base_prompt = hub.pull("langchain-ai/openai-functions-template")
# prompt = base_prompt.partial(instructions=instructions)
# llm = ChatOpenAI(temperature=0)

# agent = create_openai_functions_agent(llm, tools, prompt)
# agent_executor = AgentExecutor(
#     agent=agent,
#     tools=tools,
#     verbose=True,
#     return_intermediate_steps=True
# )

# def process_chat(agent_executor, user_input, chat_history):
#     response = agent_executor.invoke({
#         "input": user_input,
#         "chat_history": chat_history
#     })
#     return [response["output"], response['intermediate_steps'][0]]

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

# Facebook Manager
class FacebookManager:
    def _init_(self):
        self.credentials = self._load_credentials()
        self.facebook_api = self._initialize_facebook_api()

    def _load_credentials(self):
        try:
            with open('facebook_token.json', 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError("Token file not found")
        except json.JSONDecodeError:
            raise ValueError("Error decoding the token file")

    def _initialize_facebook_api(self):
        access_token = self.credentials.get('page_access_token')
        if not access_token:
            raise ValueError("Page access token is missing")
        return facebook.GraphAPI(access_token)

    def generate_facebook_content(self, content):
        # Replace this with your content generation logic
        return f"Generated Facebook Post: {content}"

    def post_to_facebook(self, content):
        try:
            post = self.facebook_api.put_object(parent_object='me', connection_name='feed', message=str(content))
            return {'success': True, 'post_id': post['id'], 'message': 'Post successful!'}
        except facebook.GraphAPIError as e:
            return {'success': False, 'error': str(e)}
        except Exception as e:
            return {'success': False, 'error': f'An unexpected error occurred: {e}'}
        # def post_to_facebook(self, content):
#         try:
#             generate = fb.run(content)
#             post = self.facebook_api.put_object(parent_object='me', connection_name='feed', message=str(generate))
#             return {'message': 'Post successful', 'post_id': post['id']}
#         except facebook.GraphAPIError as e:
#             return {'error': str(e)}
#         except Exception as e:
#             return {'error': f'An unexpected error occurred: {e}'}
class discordOauth:
    def _init_(self):
        self.client = APIClient(token=TOKEN, client_secret=CLIENT_SECRET)
    
    def start_oauth(self):
        return redirect(OAUTH_URL)

    def callback(self):
        print("Request Args:", request.args)
        if 'code' not in request.args:
            return "Error: Missing 'code' parameter in the request.", 400
        print("1jbbkjbnkjnkjvhjbn ")
        code = request.args['code']
        print("1")
        access_token = self.client.oauth.get_access_token(code, REDIRECT_URI).access_token
        print("2")

        bearer_client = APIClient(access_token, bearer=True)
        current_user = bearer_client.users.get_current_user()

        self.store_data({
            'access_token': access_token,
            'current_user': {
                'id': current_user.id,
                'username': current_user.username,
                'discriminator': current_user.discriminator,
                'avatar': current_user.avatar_url
            }
        })
        return redirect("/http://localhost:5174/Automation")

    def get_stored_data(self):
        if os.path.exists('discord_access.json'):
            with open('discord_access.json', 'r') as f:
                return json.load(f)
        return None

    def store_data(self, data):
        with open('discord_access.json', 'w') as f:
            json.dump(data, f)

@app.route('/discord/connect', methods=['GET'])
def discord_connect():
    try:
        disc = discordOauth()
        return disc.start_oauth()  # Start the OAuth flow by redirecting the user
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/discord/callback', methods=['GET'])
def discord_callback():
    try:
        disc = discordOauth()
        return disc.callback()  # Handle the OAuth callback and store user data
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/youtube/connect', methods=['GET'])
def youtube_connect():
    try:
        ytcn= YouTubeUploader()
        service = ytcn.get_authenticated_service() # Call your authentication function
        return jsonify({"success": True, "message": "YouTube connected successfully!"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
@app.route('/generate_facebook_content', methods=['POST'])
def generate_facebook_content():
    data = request.get_json()
    text = data.get('text')
    if not text:
            return jsonify({'error': 'Text is required to generate a fb post'}), 400

    facebook_manager = Facebook()
    generated_content = facebook_manager.run(text)
    if not generated_content:
            
            app.logger.error('Failed to generate tweet: No result returned')
            return jsonify({'error': 'Failed to generate post'}), 500
    content = generated_content  # Adjust based on your Crewai implementation
    
    return jsonify({'content': str(content)})

@app.route('/youtube_upload', methods=['POST'])
def upload_video():
    content = request.form['content']
    video_file = request.files['file']
    
    file_path = os.path.join('uploads', video_file.filename)
    video_file.save(file_path)
    
    title_creator = YouTubeTitleCreator()
    description_creator = YouTubeDescriptCreator()
    
    video_title = title_creator.run(str(content))
    video_description = description_creator.run(str(content))
    
    uploader = YouTubeUploader()
    uploader.set_content(title=str(video_title), description=str(video_description))
    result = uploader.upload(file_path)
    
    return jsonify({"message": result})

# @app.route('/post_facebook', methods=['POST'])
# def post_facebook():
#     try:
#         # Retrieve stored data (like access token)
#         data = get_stored_data()
#         if not data:
#             return jsonify({'success': False, 'message': 'No stored Facebook access token found.'})

#         access_token = data.get('access_token')
#         if not access_token:
#             return jsonify({'success': False, 'message': 'No access token found in stored data.'})

#         # Get the content of the Facebook post from the request
#         post_content = request.get_json().get('content')
#         if not post_content:
#             return jsonify({'success': False, 'message': 'Post content is required'})

#         # Set up OAuth2 session with the access token
#         token = {'access_token': access_token}
#         client = OAuth2Session(client_id=os.getenv('FACEBOOK_CLIENT_ID'), token=token)

#         # Post the content to Facebook
#         response = client.post(
#             "https://graph.facebook.com/v12.0/me/feed",
#             json={"message": post_content}
#         )

#         # Handle response
#         if response.status_code == 200:
#             return jsonify({'success': True, 'message': 'Facebook post created successfully!'})
#         else:
#             return jsonify({'success': False, 'message': f'Failed to post on Facebook: {response.text}'})
#     except Exception as e:
#         return jsonify({'success': False, 'message': str(e)}), 500

def create_tables():
    with app.app_context():
        db.create_all()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/user/signup', methods=['POST'])
def signup():
    data = request.form
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    file = request.files.get('photo')

    if not username or not email or not password:
        return jsonify({'success': False, 'message': 'Please fill in all fields'})

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({'success': False, 'message': 'User already exists'})

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
    else:
        filename = None

    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    new_user = User(username=username, email=email, password=hashed_password, photo=filename)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'success': True, 'message': 'User registered successfully'})
# Load the text classification pipeline


@app.route('/plagiarism', methods=['POST'])
def home():
    result = None
    if request.method == 'POST':
        text = request.json['text']  # Changed from form to json
        result = pipe(text)
        return jsonify({"result": result})  # Return the result as JSON
    
    return jsonify({"error": "Invalid request"}), 400
@app.route('/user/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'success': False, 'message': 'Please fill in all fields'})

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'success': False, 'message': 'User does not exist'})

    if not check_password_hash(user.password, password):
        return jsonify({'success': False, 'message': 'Incorrect password'})

    return jsonify({'success': True, 'message': 'Login successful', 'username': user.username, 'photo': user.photo})

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/summarize_youtube', methods=['POST'])
def summarize_youtube():
    data = request.json
    youtube_link = data.get('youtube_link')

    if not youtube_link:
        return jsonify({'success': False, 'message': 'YouTube link is required'})

    try:
        summarizer = YouTubeTranscriptSummarizer()
        summary = summarizer.process_video(youtube_link)

        if not summary:
            return jsonify({'success': False, 'message': 'Failed to generate summary'})

        output_path = 'outputs/ytVideoSummarizer/youtube_summary.md'
        with open(output_path, 'w') as file:
            file.write(summary)
        
        # Confirm the file was saved
        if os.path.isfile(output_path):
            return jsonify({'success': True, 'summary': summary})
        else:
            return jsonify({'success': False, 'message': 'Failed to save the summary file'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/summary/<filename>', methods=['GET'])
def get_summary(filename):
    file_path = os.path.join('outputs/ytVideoSummarizer', filename)
    if not os.path.isfile(file_path):
        return jsonify({'success': False, 'message': 'File not found'}), 404

    return send_from_directory('outputs/ytVideoSummarizer', filename)
@app.route('/outputs/<path:filename>')
def serve_output(filename):
    return send_from_directory('outputs', filename)
# Twitter OAuth functions
def create_code_verifier():
    code_verifier = base64.urlsafe_b64encode(os.urandom(30)).decode("utf-8")
    return re.sub("[^a-zA-Z0-9]+", "", code_verifier)

def create_code_challenge(code_verifier):
    code_challenge = hashlib.sha256(code_verifier.encode("utf-8")).digest()
    return base64.urlsafe_b64encode(code_challenge).decode("utf-8").replace("=", "")

code_verifier = create_code_verifier()
code_challenge = create_code_challenge(code_verifier)

@app.route('/start_twitter_oauth')
def start_twitter_oauth():
    twitter = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scopes)
    authorization_url, state = twitter.authorization_url(
        auth_url, code_challenge=code_challenge, code_challenge_method="S256"
    )
    session["oauth_state"] = state
    return redirect(authorization_url)
@app.route('/linkedin/check_connected', methods=['GET'])
def linkedin_check_connected():
    if os.path.exists('linkedin_token.json'):
        return jsonify({'connected': True})
    return jsonify({'connected': False})

@app.route('/oauth/callback')
def twitter_callback():
    try:
        code = request.args.get("code")
        if not code:
            return "No authorization code found in the request."

        twitter = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scopes)
        token = twitter.fetch_token(
            token_url=token_url,
            client_secret=client_secret,
            code_verifier=code_verifier,
            code=code,
        )

        bearer_client = OAuth2Session(client_id, token=token)
        user_info_response = bearer_client.get('https://api.twitter.com/2/users/me')
        if user_info_response.status_code != 200:
            return "Failed to fetch user info."

        user_info = user_info_response.json()
        if 'data' not in user_info:
            return "User info does not contain 'data'."

        user_data = user_info['data']
        session['token'] = token
        session['current_user'] = {
            'id': user_data['id'],
            'username': user_data['username'],
            'name': user_data['name'],
        }

        store_data = {
            'access_token': token['access_token'],
            'current_user': session['current_user'],
        }

        with open('twitter_access.json', 'w') as f:
            json.dump(store_data, f)

        return redirect('http://localhost:5173/Automation')  # Change to your frontend's home route
    except Exception as e:
        return str(e)

def get_stored_data():
    try:
        with open('twitter_access.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return None
@app.route('/post_facebook', methods=['POST'])
def post_to_facebook():
    content = request.json.get('content')
    if not content:
        return jsonify({'error': 'Content is required'}), 400

    facebook_manager = FacebookManager()
    result = facebook_manager.post_to_facebook(content)
    
    if not result.get('success'):
        return jsonify(result), 500
    
    return jsonify(result)

@app.route('/generate_tweet', methods=['POST'])
def generate_tweet():
    try:
        data = request.get_json()
        text = data.get('text')  # Correctly fetch the 'text' key from the JSON data
        if not text:
            return jsonify({'error': 'Text is required to generate a tweet'}), 400

        # Initialize the Twitter class
        twitter = Twitter()
        # Generate the tweet using Crewai
        result = twitter.run(text)
        if not result:
            app.logger.error('Failed to generate tweet: No result returned')
            return jsonify({'error': 'Failed to generate tweet'}), 500

        # Assuming result is a string or has an 'output' attribute
        tweet = result  # Adjust based on your Crewai implementation
        return jsonify({'tweet': str(tweet)})
    except Exception as e:
        app.logger.error(f'Error in generate_tweet route: {str(e)}')
        return jsonify({'error': str(e)}), 500

@app.route('/post_tweet', methods=['POST'])
def post_tweet():
    try:
        # Retrieve stored data (like access token)
        data = get_stored_data()
        if not data:
            return jsonify({'success': False, 'message': 'No stored Twitter access token found.'})

        access_token = data.get('access_token')
        if not access_token:
            return jsonify({'success': False, 'message': 'No access token found in stored data.'})

        # Get the content of the tweet from the request
        tweet_content = request.get_json().get('tweet')
        if not tweet_content:
            return jsonify({'success': False, 'message': 'Tweet content is required'})

        # Set up OAuth2 session with the access token
        token = {'access_token': access_token}
        client = OAuth2Session(client_id=os.getenv('TWITTER_CLIENT_ID'), token=token)

        # Post the tweet
        response = client.post(
            "https://api.twitter.com/2/tweets",
            json={"text": tweet_content}
        )

        # Handle response
        if response.status_code == 201:
            return jsonify({'success': True, 'message': 'Tweet posted successfully!'})
        else:
            return jsonify({'success': False, 'message': f'Failed to post tweet: {response.text}'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve(path):
    if path and os.path.exists("frontend/build/" + path):
        return send_from_directory("frontend/build", path)
    else:
        return send_from_directory("frontend/build", "index.html")

@app.route('/check_twitter_connection', methods=['GET'])
def check_twitter_connection():
    if os.path.exists('twitter_access.json'):
        return {'connected': True}
    return {'connected': False}
@app.route('/linkedin/login')
def linkedin_login():
    session.clear()
    authorization_url = 'https://www.linkedin.com/oauth/v2/authorization'
    params = {
        'response_type': 'code',
        'client_id': linkedin_client_id,
        'redirect_uri': linkedin_redirect_uri,
        'scope': 'openid+profile+email+w_member_social'
    }
    url = f"{authorization_url}?response_type={params['response_type']}&client_id={params['client_id']}&redirect_uri={params['redirect_uri']}&scope={params['scope']}"
    return redirect(url)

@app.route('/linkedin/callback')
def linkedin_callback():
    code = request.args.get('code')
    
    if code:
        user = session.get('user_id')
        access_token = get_linkedin_access_token(code)
        if access_token:
            session['linkedin_access_token'] = access_token
            uid = get_linkedin_id(access_token)
            with open("linkedin_token.json", "w") as f:
                json.dump({"access_token": access_token, "id": uid}, f)
            return 'Linkedin oauth very succesful'
            
        else:
            return 'Failed to get access token!'
    else:
        return 'LinkedIn OAuth failed!'
  
def get_linkedin_access_token(code):
    access_token_url = 'https://www.linkedin.com/oauth/v2/accessToken'
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': linkedin_redirect_uri,
        'client_id': linkedin_client_id,
        'client_secret': linkedin_client_secret
    }
    response = requests.post(access_token_url, data=data)
    print(f"Response from LinkedIn access token request: {response.json()}")
    return response.json().get('access_token')

def get_linkedin_id(access_token):
    url = 'https://api.linkedin.com/v2/userinfo'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers)
    return response.json().get('sub')
@app.route('/generate_linkedin_content', methods=['POST'])
def generate_linkedin_content():
    try:
        # Extract content from request
        content = request.form.get('content')
        image = request.files.get('image')

        if not content:
            return jsonify({'error': 'Content is required to generate a LinkedIn post'}), 400

        # Initialize LinkedIn content generation
        l_crew = CrewLinkedIn()
        generated_content = l_crew.run(content)  # Generate content using Crewai

        # Prepare image if provided
        image_path = None
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(image_path)
            # Construct the image URL (assuming a static file server setup)
            image_url = request.host_url + 'uploads/' + filename
        else:
            image_url = None

        # Return generated content and image URL
        return jsonify({'content': str(generated_content), 'image_url': image_url})

    except Exception as e:
        app.logger.error(f'Error in generate_linkedin_content route: {str(e)}')
        return jsonify({'error': str(e)}), 500

@app.route('/post_linkedin', methods=['POST'])
def post_linkedin():
    try:
        content = request.form.get('content')
        image = request.files.get('image')

        if not content:
            return jsonify({'success': False, 'message': 'Content is required to post to LinkedIn.'})

        # Save the image if provided
        image_path = None
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(image_path)

        # Initialize LinkedIn manager and post content
        linkedin_manager = LinkedinManager()
        response = linkedin_manager.post_to_linkedin(content, image_path)

        # Handle response
        
        return jsonify({'success': True, 'message': 'Post published to LinkedIn', 'response': response})
        # else:
        #     return jsonify({'success': False, 'message': f'Failed to post content to LinkedIn: {response.text}'})
    except Exception as e:
        app.logger.error(f'Error in post_linkedin route: {str(e)}')
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/draft_email', methods=['POST'])
def draft_email():
    
    data = request.get_json()
    
    user_input = data.get('user_input', '')
    user_input= user_input+"sent by Fazil S"
    chat_history = data.get('chat_history', '[]')

    if chat_history:
        chat_history = loads(chat_history)
    else:
        chat_history = []

    response = process_chat(agent_executor, user_input, chat_history)

    chat_history.append(HumanMessage(content=user_input))
    chat_history.append(AIMessage(content=response[0]))

    history = dumps(chat_history)
    return jsonify({
        'output': response[0],
        'chat_history': history,
        'tool_input': response[1][0].tool_input['message']
    })

if __name__ == '__main__':
        port = int(os.environ.get("PORT", 5000))
        app.run(host='0.0.0.0', port=port)