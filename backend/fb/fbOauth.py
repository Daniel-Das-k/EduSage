from flask import Flask, redirect, request, session, url_for
import requests
import os
import json

app = Flask(__name__)
app.secret_key = "secret"
Fb_APP_ID = "1519269175630468"
Fb_APP_SECRET = "e04ebcfe52882ed9a9134937547e0ba0"
Fb_REDIRECT_URI = "https://facebook-rakb.onrender.com/facebook/callback"

@app.route('/')
def home():
    access_token = session.get("access_token")
    page_access_token = session.get("page_access_token")
    if access_token and page_access_token:
        return f'''
            User Access Token: {access_token}
            Page Access Token: {page_access_token}
        '''
    else:
        return redirect(url_for('facebook_login'))

@app.route('/facebook/login')
def facebook_login():
    return redirect(f"https://www.facebook.com/v20.0/dialog/oauth?client_id={Fb_APP_ID}&redirect_uri={Fb_REDIRECT_URI}&scope=read_insights,publish_video,pages_manage_instant_articles,pages_show_list,pages_messaging,instagram_basic,instagram_manage_comments,instagram_manage_insights,instagram_content_publish,page_events,pages_read_engagement,pages_read_user_content,pages_manage_metadata,pages_manage_posts,pages_manage_engagement,instagram_manage_events")

@app.route('/facebook/callback')
def facebook_callback():
    code = request.args.get("code")
    if code:
        response = requests.get(
            f"https://graph.facebook.com/v20.0/oauth/access_token?client_id={Fb_APP_ID}&redirect_uri={Fb_REDIRECT_URI}&client_secret={Fb_APP_SECRET}&code={code}"
        )
        print("Response: ",response)
        data = response.json()
        if "access_token" in data:
            user_access_token = data["access_token"]
            session["access_token"] = user_access_token

            pages_response = requests.get(
                f"https://graph.facebook.com/v20.0/me/accounts?access_token={user_access_token}"
            )
            pages_data = pages_response.json()
            if 'data' in pages_data:
                print("Pages Data :",pages_data)
                first_page = pages_data['data'][0]
                page_access_token = first_page['access_token']
                session["page_access_token"] = page_access_token
                session["page_id"] = first_page['id']
                return redirect(url_for('home'))
            else:
                error_message = pages_data.get('error', {}).get('message', 'Unknown error')
                return f"Error fetching pages: {error_message}"
        else:
            error_message = data.get('error', {}).get('message', 'Unknown error')
            return f"Error fetching user access token: {error_message}"
    else:
        return "Error: No code provided or invalid code"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5002))
    app.run(host='0.0.0.0', port=port)