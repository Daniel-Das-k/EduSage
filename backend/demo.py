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
