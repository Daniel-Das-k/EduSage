import os
import json
from flask import Flask, render_template, request, session, redirect
from zenora import APIClient
from flask_cors import CORS
from .creds import TOKEN, CLIENT_SECRET, REDIRECT_URI, OAUTH_URL


class discordOauth:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.config["SECRET_KEY"] = "verysecret"
        CORS(self.app)
        self.client = APIClient(token=TOKEN, client_secret=CLIENT_SECRET)
        self.setup_routes()

    def setup_routes(self):
        self.app.add_url_rule('/', 'home', self.home,methods=['GET', 'POST'])
        self.app.add_url_rule('/oauth/callback', 'callback', self.callback,methods=['GET'])
        self.app.add_url_rule('/logout', 'logout', self.logout,methods=['GET'])

    def home(self):
        stored_data = self.get_stored_data()
        if stored_data:
            session['token'] = stored_data['access_token']
            current_user = stored_data['current_user']
            print(current_user, "User data loaded from storage")
            return render_template("index.html", current_user=current_user)
        return render_template("index.html", oauth_uri=OAUTH_URL)

    def callback(self):
       
        print("Request Args:", request.args)
        if 'code' not in request.args:
            return "Error: Missing 'code' parameter in the request.", 400

        code = request.args['code']
        print("1")
        access_token = self.client.oauth.get_access_token(code, REDIRECT_URI).access_token
        print("2")
        session['token'] = access_token

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
        return redirect("/")

    def logout(self):
        session.clear()
        if os.path.exists('discord_access.json'):
            os.remove('discord_access.json')
        return redirect("/")


    def get_stored_data(self):
        if os.path.exists('discord_access.json'):
            with open('discord_access.json', 'r') as f:
                return json.load(f)
        return None

    def store_data(self, data):
        with open('discord_access.json', 'w') as f:
            json.dump(data, f)

    def run(self, debug=True):
        self.app.run(debug=debug)

if __name__ == "__main__":
    app = discordOauth()
    app.run()
