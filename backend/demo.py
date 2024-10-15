import os
from flask import Flask, request, jsonify, send_from_directory
from yt_dlp import YoutubeDL
import whisper
import torch
import subprocess
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from googletrans import Translator
from gtts import gTTS
import requests
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate

from langchain.text_splitter import RecursiveCharacterTextSplitter
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/": {"origins": ""}})  # Enable CORS for all routes
GOOGLE_GEMINI_KEY='AIzaSyBlOBWJSuYpQG4a3RnESjdiUR2UgpZhaZs'
# Ensure that the Whisper model runs on GPU if available
device = "cuda" if torch.cuda.is_available() else "cpu"
model = whisper.load_model("base").to(device)
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
# Create a directory to serve static files
STATIC_DIR = 'static'
os.makedirs(STATIC_DIR, exist_ok=True)

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks

def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=GOOGLE_GEMINI_KEY)
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")
def get_conversational_chain():
    prompt_template = """   
    Answer the question as detailed as possible from the provided context, make sure to provide all the details, if the answer is not in
    provided context try to relate it with context and provide answer, but don't provide the wrong answer.\n\n
    Context:\n {context}?\n
    Question: \n{question}\n

    Answer:
    """

    model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3, google_api_key=GOOGLE_GEMINI_KEY)
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)

    return chain

def user_input(user_question):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=GOOGLE_GEMINI_KEY)
   
    new_db_files = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    
    docs = new_db_files.similarity_search(user_question, k=10)
    
    chain = get_conversational_chain()

    response = chain(
        {"input_documents": docs, "question": user_question}, return_only_outputs=True
    )

    return response["output_text"]
def translate_fn(lang,text):
    translator = Translator()
    translate=translator.translate(text=text, dest=lang)
    return translate.text

def download_audio_from_youtube(url, output_path='.'):
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{output_path}/sample.%(ext)s',
        'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'wav'}],
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    
    return os.path.join(output_path, "sample.wav")

def convert_audio_for_transcription(input_filename):
    output_filename = os.path.join(os.path.dirname(input_filename), "temp_converted.wav")
    try:
        subprocess.run(['ffmpeg', '-i', input_filename, '-ar', '16000', '-ac', '1', output_filename], check=True)
        return output_filename
    except subprocess.CalledProcessError as e:
        print(f"Error converting audio: {e}")
        return None

def transcribe_audio_file(audio_filename):
    temp_filename = convert_audio_for_transcription(audio_filename)
    if temp_filename:
        try:
            result = model.transcribe(temp_filename, fp16=torch.cuda.is_available())
            os.remove(temp_filename)
            return result['text']
        except Exception as e:
            print(f"Error transcribing audio file {audio_filename}: {e}")
            os.remove(temp_filename)
            return "[Error processing the audio file]"
    else:
        return "[Conversion failed, no transcription performed]"

def text_to_speech(text, lang_code):
    tts = gTTS(text=text, lang=lang_code, slow=False)
    output_file = os.path.join(STATIC_DIR, f"output_{lang_code}.mp3")
    tts.save(output_file)
    return output_file

@app.route('/process', methods=['POST'])
def process():
    print("hello")
    data = request.json
    
    youtube_url = data.get("youtube_url")
    print("hello")

    if youtube_url:
        # Download and transcribe
        audio_file = download_audio_from_youtube(youtube_url)
        transcript = transcribe_audio_file(audio_file)
        print(transcript)
        text = get_text_chunks(transcript)
        get_vector_store(text)
                                             
        # Translate
        
        translated_text = translate_fn('ta',transcript)
        # Convert to speech
        output_audio_file = text_to_speech(translated_text, 'ta')
        print('tts done ')
        return jsonify({
            "transcript": transcript,
            "translated_text": translated_text,
            "audio_url": f"/static/{os.path.basename(output_audio_file)}"
        })

    return jsonify({"error": "YouTube URL not provided"}), 400
@app.route('/answer', methods=['POST'])
def answer():
    # Get question from frontend
    data = request.json
    user_question = data.get("question")

    if user_question:
        # Generate an answer
        try:
            answer = user_input(user_question)
            return jsonify({"answer": answer})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return jsonify({"error": "No question provided"}), 400

@app.route('/static/<path:filename>', methods=['GET'])
def serve_static(filename):
    return send_from_directory(STATIC_DIR, filename, mimetype='audio/mpeg')

if __name__ == '__main__':
    app.run(debug=True)
# import os
# from flask import Flask, request, jsonify, send_from_directory
# from yt_dlp import YoutubeDL
# import whisper
# import torch
# import subprocess
# from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
# from googletrans import Translator
# from gtts import gTTS
# import requests
# from langchain_google_genai import GoogleGenerativeAIEmbeddings
# from langchain_community.vectorstores import FAISS
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain.chains.question_answering import load_qa_chain
# from langchain.prompts import PromptTemplate

# from langchain.text_splitter import RecursiveCharacterTextSplitter

# from flask_cors import CORS

# app = Flask(__name__)
# CORS(app)  # Enable CORS for all routes

# # Ensure that the Whisper model runs on GPU if available
# # device = "cuda" if torch.cuda.is_available() else "cpu"
# # model = whisper.load_model("base").to(device)
# model=None
# # Create a directory to serve static files
# STATIC_DIR = 'static'
# os.makedirs(STATIC_DIR, exist_ok=True)
# GOOGLE_GEMINI_KEY='AIzaSyBlOBWJSuYpQG4a3RnESjdiUR2UgpZhaZs'

# def translate_fn(lang,text):
#     translator = Translator()
#     translate=translator.translate(text=text, dest=lang)
#     return translate.text

# def download_audio_from_youtube(url, output_path='.'):
#     if not os.path.exists(output_path):
#         os.makedirs(output_path)
    
#     ydl_opts = {
#         'format': 'bestaudio/best',
#         'outtmpl': f'{output_path}/sample.%(ext)s',
#         'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'wav'}],
#     }

#     with YoutubeDL(ydl_opts) as ydl:
#         ydl.download([url])
    
#     return os.path.join(output_path, "sample.wav")

# def convert_audio_for_transcription(input_filename):
#     output_filename = os.path.join(os.path.dirname(input_filename), "temp_converted.wav")
#     try:
#         subprocess.run(['ffmpeg', '-i', input_filename, '-ar', '16000', '-ac', '1', output_filename], check=True)
#         return output_filename
#     except subprocess.CalledProcessError as e:
#         print(f"Error converting audio: {e}")
#         return None
    
# def get_text_chunks(text):
#     text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
#     chunks = text_splitter.split_text(text)
#     return chunks

# def get_vector_store(text_chunks):
#     embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=GOOGLE_GEMINI_KEY)
#     vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
#     vector_store.save_local("faiss_index")
# def get_conversational_chain():
#     prompt_template = """   
#     Answer the question as detailed as possible from the provided context, make sure to provide all the details, if the answer is not in
#     provided context try to relate it with context and provide answer, but don't provide the wrong answer.\n\n
#     Context:\n {context}?\n
#     Question: \n{question}\n

#     Answer:
#     """

#     model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3, google_api_key=GOOGLE_GEMINI_KEY)
#     prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
#     chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)

#     return chain

# def user_input(user_question):
#     embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=GOOGLE_GEMINI_KEY)
   
#     new_db_files = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    
#     docs = new_db_files.similarity_search(user_question, k=10)
    
#     chain = get_conversational_chain()

#     response = chain(
#         {"input_documents": docs, "question": user_question}, return_only_outputs=True
#     )

#     return response["output_text"]


# def transcribe_audio_file(audio_filename):
#     temp_filename = convert_audio_for_transcription(audio_filename)
#     if temp_filename:
#         try:
#             result = model.transcribe(temp_filename, fp16=torch.cuda.is_available())
#             os.remove(temp_filename)
#             return result['text']
#         except Exception as e:
#             print(f"Error transcribing audio file {audio_filename}: {e}")
#             os.remove(temp_filename)
#             return "[Error processing the audio file]"
#     else:
#         return "[Conversion failed, no transcription performed]"

# def text_to_speech(text, lang_code):
#     tts = gTTS(text=text, lang=lang_code, slow=False)
#     output_file = os.path.join(STATIC_DIR, f"output_{lang_code}.mp3")
#     tts.save(output_file)
#     return output_file

# @app.route('/process', methods=['POST'])
# def process():
#     print("hello")
#     data = request.json
    
#     youtube_url = data.get("youtube_url")
#     print("hello")

#     if youtube_url:
#         # Download and transcribe
#         audio_file = download_audio_from_youtube(youtube_url)
#         transcript = transcribe_audio_file(audio_file)
#         text=get_text_chunks(transcript)
#         get_vector_store(text)
#         # Translate
#         # transcript='''the depths of neural networks, a subfield of machine learning inspired by the human brain, this content delves into their remarkable abilities. Through a constructed neural network, the process of differentiating shapes is demonstrated, showcasing the intricate computations performed within its layers. From facial recognition to music composition, the versatile applications of neural networks are highlighted, emphasizing their pattern recognition and prediction capabilities. The training process, involving forward and back propagation, is described, explaining how neural networks adjust their weights to minimize errors. Remarkably, neural networks can even mimic human behavior, leading to questions about their potential to replicate the human brain's complexities.'''
        
#         translated_text = translate_fn('ta',transcript)
#         # translated_text='''கடந்த கோடையில், என் குடும்பத்தினருடன் ரஷ்யாவுக்குச் சென்றேன். எங்களில் யாரும் ர             ரஷ்ய மொழியைப் படிக்கத் தெரியாவிட்டாலும், எங்களால் வழியைக் கண்டுபிடிக்க முடிந்தது. ரஷ்ய மொழி பலகைகளை ஆங்             கிலத்தில் உண்மையான நேரத்தில் மொழிபெயர்த்ததற்கு கூகுள் நன்றி. இது நரம்பு வலைப்பின்னல்களின் பல பயன்பாடுக               களில் ஒன்றாகும். நரம்பு வலைப்பின்னல்கள் ஆழமான கற்றலின் அடிப்படையை உருவாக்குகின்றன, இது மனித மூளையின் அம             மைப்பால் ஈர்க்கப்பட்ட வழிமுறைகளைக் கொண்ட துணை நிரப்பப்பட்ட இயந்திரக் கற்றலாகும். நரம்பு வலைப்பின்னல்கள்                    தரவை எடுத்துக்கொண்டு, இந்தத் தரவில் உள்ள வடிவங்களை அடையாளம் காண தங்களைத் தாங்களே பயிற்றுவித்து, பின்ன              னர் புதிய தரவுத் தொகுப்பிற்கான வெளியீடுகளை முன்னறிவிக்கின்றன. இது எவ்வாறு செய்யப்படுகிறது என்பதைப் புரி            ிந்துகொள்வோம். ஒரு சதுரம், வட்டம் மற்றும் முக்கோணம் ஆகியவற்றை வேறுபடுத்திப் பார்க்கும் ஒரு நரம்பு வலைப்                 பின்னலை உருவாக்குவோம். நரம்பு வலைப்பின்னல்கள் நரம்பு செல்களின் அடுக்குகளால் ஆனவை. இந்த நரம்பு செல்கள்                  வலைப்பின்னலின் முக்கிய செயலாக்க அலகுகள் ஆகும். முதலில், உள்ளீட்டைப் பெறும் உள்ளீட்டு அடுக்கு நம்மிடம்                    உள்ளது. வெளியீட்டு அடுக்கு எங்கள் இறுதி வெளியீட்டை முன்னறிவிக்கிறது. இடையில், எங்கள் வலைப்பின்னலுக்குத               த் தேவையான பெரும்பாலான கணக்கீடுகளைச் செய்யும் மறைக்கப்பட்ட அடுக்குகள் உள்ளன. இதோ ஒரு வட்டத்தின் படம். இ                இந்தப் படம் 28x28 பிக்சல்களால் ஆனது, இது 784 பிக்சல்களைக் கொண்டுள்ளது. ஒவ்வொரு பிக்சலும் முதல் அடுக்கின               ன் ஒவ்வொரு நரம்பு செல்லுக்கும் உள்ளீடாக வழங்கப்படுகிறது. ஒரு அடுக்கின் நரம்பு செல்கள் சேனல்கள் மூலம் அட                 டுத்த அடுக்கின் நரம்பு செல்களுடன் இணைக்கப்படுகின்றன. இந்த சேனல்களில் ஒவ்வொன்றும் எடை எனப்படும் ஒரு எண்ண                 ணியல் மதிப்புக்கு ஒதுக்கப்படுகிறது. உள்ளீடுகள் தொடர்புடைய எடைகளால் பெருக்கப்படுகின்றன, அவற்றின் கூட்டுத               த்தொகை மறைக்கப்பட்ட அடுக்கில் உள்ள நரம்பு செல்களுக்கு உள்ளீடாக அனுப்பப்படுகிறது. இந்த நரம்பு செல்களில்                   ஒவ்வொன்றும் பட்சபாதம் எனப்படும் எண்ணியல் மதிப்புடன் தொடர்புடையது, இது பின்னர் உள்ளீட்டுத் தொகையில் சேர                  ர்க்கப்படுகிறது. இந்த மதிப்பு பின்னர் செயல்படுத்தும் சார்பு எனப்படும் வாசல் சார்பு வழியாக அனுப்பப்படுகி                ிறது. செயல்படுத்தும் சார்பின் விளைவு குறிப்பிட்ட நரம்பு செல் செயல்படுத்தப்படுமா இல்லையா என்பதை தீர்மானி               ிக்கிறது. ஒரு செயல்படுத்தப்பட்ட நரம்பு செல் சேனல்கள் வழியாக அடுத்த அடுக்கின் நரம்பு செல்களுக்கு தரவை அன              னுப்புகிறது. இந்த வழியில், தரவு வலைப்பின்னல் வழியாக பரப்பப்படுகிறது. இது முன்னோக்கி பரப்புதல் என்று அழை            ைக்கப்படுகிறது. வெளியீட்டு அடுக்கில், அதிக மதிப்புள்ள நரம்பு செல் செயல்பட்டு வெளியீட்டை தீர்மானிக்கிறது                ு. மதிப்புகள் அடிப்படையில் ஒரு நிகழ்தகவு ஆகும். எடுத்துக்காட்டாக, இங்கே சதுரத்துடன் தொடர்புடைய நமது நரம            ம்பு செல்லுக்கு அதிக நிகழ்தகவு உள்ளது. எனவே, அது நரம்பு வலைப்பின்னலால் முன்னறிவிக்கப்பட்ட வெளியீடு ஆகும             ம். நிச்சயமாக, அதைப் பார்த்தவுடன், எங்கள் நரம்பு வலைப்பின்னல் தவறான முன்னறிவிப்பைச் செய்துள்ளது என்பதை                   நாங்கள் அறிவோம். ஆனால் வலைப்பின்னல் இதை எவ்வாறு கண்டுபிடிக்கிறது? எங்கள் வலைப்பின்னல் இன்னும் பயிற்சி                   பெறவில்லை என்பதை கவனத்தில் கொள்ளவும். இந்தப் பயிற்சி செயல்முறையின் போது, உள்ளீட்டோடு சேர்ந்து, எங்கள்                   வலைப்பின்னலுக்கும் வெளியீடு வழங்கப்படுகிறது. முன்னறிவிக்கப்பட்ட வெளியீடு, முன்னறிவிப்பில் உள்ள பிழையை                 உணர உண்மையான வெளியீட்டுடன் ஒப்பிடப்படுகிறது. பிழையின் அளவு நாம் எவ்வளவு தவறாக இருக்கிறோம் என்பதைக் குற            றிக்கிறது, மேலும் அடையாளம் நமது முன்னறிவிக்கப்பட்ட மதிப்புகள் எதிர்பார்த்ததை விட அதிகமாகவோ அல்லது குறைவ            வாகவோ உள்ளதா என்பதைக் குறிக்கிறது. பிழையைக் குறைக்க திசை மற்றும் மாற்றத்தின் அளவைக் குறிக்கும் அம்புகள்                இங்கே உள்ளன. இந்தத் தகவல் பின்னர் எங்கள் வலைப்பின்னல் வழியாக பின்னோக்கி மாற்றப்படுகிறது. இது பின்னோக்                 கி பரப்புதல் என்று அழைக்கப்படுகிறது. இப்போது, இந்தத் தகவலை அடிப்படையாகக் கொண்டு, எடைகள் சரிசெய்யப்படுக             கின்றன. முன்னோக்கி பரப்புதல் மற்றும் பின்னோக்கி பரப்புதலின் இந்த சுழற்சி பல உள்ளீடுகளுடன் தொடர்ந்து செய                 ய்யப்படுகிறது. இந்த செயல்முறை எங்கள் எடைகள் ஒதுக்கப்படும் வரை தொடர்கிறது, இதனால் பெரும்பாலான சந்தர்ப்பங               ங்களில் வலைப்பின்னல் வடிவங்களை சரியாக முன்னறிவிக்க முடியும். இது எங்கள் பயிற்சி செயல்முறையை முடிவுக்குக             க் கொண்டுவருகிறது. இந்தப் பயிற்சி செயல்முறை எவ்வளவு நேரம் ஆகும் என்று நீங்கள் யோசிக்கலாம். உண்மையாகச் ச                சொல்வதானால், நரம்பு வலைப்பின்னல்கள் பயிற்சி பெற மணிநேரங்கள் அல்லது மாதங்கள் கூட ஆகலாம். ஆனால் அதன் நோக்                கத்துடன் ஒப்பிடும்போது நேரம் ஒரு நியாயமான சமரசமாகும். நரம்பு வலைப்பின்னல்களின் சில முதன்மை பயன்பாடுகளை            ைப் பார்ப்போம். முக அங்கீகாரம். ஸ்மார்ட்போன்களில் உள்ள கேமராக்கள் ஒருவரின் முக அம்சங்களை அடிப்படையாகக்                     கொண்டு அவர்களின் வயதை மதிப்பிட முடியும். இது நரம்பு வலைப்பின்னல்கள் விளையாடுகிறது, முதலில் முகத்தை பின           ன்னணியிலிருந்து வேறுபடுத்தி, பின்னர் உங்கள் முகத்தில் உள்ள கோடுகள் மற்றும் புள்ளிகளை சாத்தியமான வயதுடன்                தொடர்புபடுத்துகிறது. முன்னறிவிப்பு. நரம்பு வலைப்பின்னல்கள் வடிவங்களைப் புரிந்து கொள்ளவும், மழைப்பொழிவ              வு அல்லது பங்கு விலைகளில் ஏற்படும் சாத்தியத்தை அதிக துல்லியத்துடன் கண்டறியவும் பயிற்சி அளிக்கப்படுகின்ற               றன. இசை இயற்றல். நரம்பு வலைப்பின்னல்கள் இசையில் உள்ள வடிவங்களைக் கூட கற்றுக்கொண்டு, புதிய இசையை இயற்ற ப              போதுமான அளவு தங்களைத் தாங்களே பயிற்றுவிக்க'''
        
# # '''
#         # Convert to speech
        
#         output_audio_file = text_to_speech(translated_text, 'ta')
#         print('tts done ')
#         return jsonify({
#             "transcript": translated_text,
#             "translated_text": translated_text,
#             "audio_url": f"/static/{os.path.basename(output_audio_file)}"
#         })

#     return jsonify({"error": "YouTube URL not provided"}), 400

# @app.route('/answer', methods=['POST'])
# def answer():
#     # Get question from frontend
#     data = request.json
#     user_question = data.get("question")

#     if user_question:
#         # Generate an answer
#         try:
#             answer = user_input(user_question)
#             return jsonify({"answer": answer})
#         except Exception as e:
#             return jsonify({"error": str(e)}), 500

#     return jsonify({"error": "No question provided"}), 400

# if __name__ == '_main_':
#     app.run(debug=True)
# import os
# from flask import Flask, request, jsonify, send_from_directory
# from yt_dlp import YoutubeDL
# import whisper
# import torch
# import subprocess
# from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
# from googletrans import Translator
# from gtts import gTTS
# import requests
# from langchain_google_genai import GoogleGenerativeAIEmbeddings
# from langchain_community.vectorstores import FAISS
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain.chains.question_answering import load_qa_chain
# from langchain.prompts import PromptTemplate
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from flask_cors import CORS

# app = Flask(__name__)
# CORS(app, resources={r"/": {"origins": ""}})  # Enable CORS for all routes
# GOOGLE_GEMINI_KEY = 'AIzaSyBlOBWJSuYpQG4a3RnESjdiUR2UgpZhaZs'

# # Ensure Whisper model runs on GPU if available
# device = "cuda" if torch.cuda.is_available() else "cpu"
# model = whisper.load_model("base").to(device)

# os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
# STATIC_DIR = 'static'
# os.makedirs(STATIC_DIR, exist_ok=True)

# def get_text_chunks(text):
#     text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
#     chunks = text_splitter.split_text(text)
#     return chunks

# def get_vector_store(text_chunks):
#     embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=GOOGLE_GEMINI_KEY)
#     vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
#     vector_store.save_local("faiss_index")

# def get_conversational_chain():
#     prompt_template = """   
#     Answer the question as detailed as possible from the provided context. Make sure to provide all the details. If the answer is not in
#     the provided context, try to relate it with context and provide an answer, but don't provide a wrong answer.\n\n
#     Context:\n {context}?\n
#     Question: \n{question}\n
#     Answer:
#     """
#     model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3, google_api_key=GOOGLE_GEMINI_KEY)
#     prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
#     chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
#     return chain

# def user_input(user_question):
#     embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=GOOGLE_GEMINI_KEY)
#     new_db_files = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
#     docs = new_db_files.similarity_search(user_question, k=10)
#     chain = get_conversational_chain()
#     response = chain(
#         {"input_documents": docs, "question": user_question}, return_only_outputs=True
#     )
#     return response["output_text"]

# def translate_fn(lang, text):
#     translator = Translator()
#     translation = translator.translate(text=text, dest=lang)
#     return translation.text

# def download_audio_from_youtube(url, output_path='.'):
#     if not os.path.exists(output_path):
#         os.makedirs(output_path)
    
#     ydl_opts = {
#         'format': 'bestaudio/best',
#         'outtmpl': f'{output_path}/sample.%(ext)s',
#         'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'wav'}],
#     }

#     with YoutubeDL(ydl_opts) as ydl:
#         ydl.download([url])
    
#     return os.path.join(output_path, "sample.wav")

# def convert_audio_for_transcription(input_filename):
#     output_filename = os.path.join(os.path.dirname(input_filename), "temp_converted.wav")
#     try:
#         subprocess.run(['ffmpeg', '-i', input_filename, '-ar', '16000', '-ac', '1', output_filename], check=True)
#         return output_filename
#     except subprocess.CalledProcessError as e:
#         print(f"Error converting audio: {e}")
#         return None

# def transcribe_audio_file(audio_filename):
#     temp_filename = convert_audio_for_transcription(audio_filename)
#     if temp_filename:
#         try:
#             # Transcribe and detect language
#             result = model.transcribe(temp_filename, fp16=torch.cuda.is_available())
#             detected_lang = result.get('language', 'en')  # Detect the source language
#             print(f"Detected language: {detected_lang}")
#             os.remove(temp_filename)
#             return result['text'], detected_lang
#         except Exception as e:
#             print(f"Error transcribing audio file {audio_filename}: {e}")
#             os.remove(temp_filename)
#             return "[Error processing the audio file]", "en"
#     else:
#         return "[Conversion failed, no transcription performed]", "en"

# def text_to_speech(text, lang_code):
#     tts = gTTS(text=text, lang=lang_code, slow=False)
#     output_file = os.path.join(STATIC_DIR, f"output_{lang_code}.mp3")
#     tts.save(output_file)
#     return output_file

# @app.route('/process', methods=['POST'])
# def process():
#     data = request.json
#     youtube_url = data.get("youtube_url")

#     if youtube_url:
#         # Download and transcribe
#         audio_file = download_audio_from_youtube(youtube_url)
#         transcript, detected_lang = transcribe_audio_file(audio_file)
#         text_chunks = get_text_chunks(transcript)
#         get_vector_store(text_chunks)
                                             
#         # Translate to Tamil (irrespective of detected language)
#         translated_text = translate_fn('ta', transcript)
        
#         # Convert to Tamil speech
#         output_audio_file = text_to_speech(translated_text, 'ta')
        
#         return jsonify({
#             "transcript": transcript,
#             "detected_language": detected_lang,
#             "translated_text": translated_text,
#             "audio_url": f"/static/{os.path.basename(output_audio_file)}"
#         })

#     return jsonify({"error": "YouTube URL not provided"}), 400

# @app.route('/answer', methods=['POST'])
# def answer():
#     # Get question from frontend
#     data = request.json
#     user_question = data.get("question")

#     if user_question:
#         try:
#             answer = user_input(user_question)
#             return jsonify({"answer": answer})
#         except Exception as e:
#             return jsonify({"error": str(e)}), 500

#     return jsonify({"error": "No question provided"}), 400

# @app.route('/static/<path:filename>', methods=['GET'])
# def serve_static(filename):
#     return send_from_directory(STATIC_DIR, filename, mimetype='audio/mpeg')

# if __name__ == '__main__':
#     app.run(debug=True)