from flask import Flask, request, jsonify
from flask_cors import CORS
import facebook
import json
from crew import Facebook

app = Flask(__name__)
CORS(app)  # Allow CORS

fb = Facebook()

class FacebookManager:
    def __init__(self):
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

    def post_to_facebook(self, content):
        try:
            generate = fb.run(content)
            post = self.facebook_api.put_object(parent_object='me', connection_name='feed', message=str(generate))
            return {'message': 'Post successful', 'post_id': post['id']}
        except facebook.GraphAPIError as e:
            return {'error': str(e)}
        except Exception as e:
            return {'error': f'An unexpected error occurred: {e}'}

@app.route('/post', methods=['POST'])
def post_to_facebook():
    content = request.json.get('content')
    if not content:
        return jsonify({'error': 'Content is required'}), 400

    facebook_manager = FacebookManager()
    result = facebook_manager.post_to_facebook(content)
    
    if 'error' in result:
        return jsonify(result), 500
    
    return jsonify(result)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5002))
    app.run(host='0.0.0.0', port=port)
