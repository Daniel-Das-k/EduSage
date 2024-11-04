# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from langchain_google_genai import GoogleGenerativeAIEmbeddings
# import google.generativeai as genai
# from langchain_community.vectorstores import FAISS
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain.chains.question_answering import load_qa_chain
# from langchain.prompts import PromptTemplate
# from PyPDF2 import PdfReader
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# import os
# from dotenv import load_dotenv

# load_dotenv()

# GOOGLE_GEMINI_KEY = os.getenv("GOOGLE_GEMINI_KEY")

# app = Flask(__name__)
# CORS(app)  # Enable CORS for all routes

# def get_pdf_text(pdf_path):
#     if os.path.isfile(pdf_path):
#         pdf_reader = PdfReader(pdf_path)
#         text = ""
#         for page in pdf_reader.pages:
#             text += page.extract_text()
#         return text
#     else:
#         raise FileNotFoundError(f"No such file: '{pdf_path}'")

# def get_text_chunks(text):
#     text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
#     chunks = text_splitter.split_text(text)
#     return chunks

# def get_vector_store(text_chunks):
#     embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001", google_api_key=GOOGLE_GEMINI_KEY)
#     vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
#     vector_store.save_local("faiss_index")

# def get_conversational_chain():
#     prompt_template = """   
#     Answer the question as detailed as possible from the provided context. Make sure to provide all the details, and if the answer is not in
#     provided context, try to relate it with context and provide an answer. But don't provide the wrong answer.\n\n
#     Context:\n {context}?\n
#     Question: \n{question}\n

#     Answer:
#     """
#     model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3, google_api_key=GOOGLE_GEMINI_KEY)
#     prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
#     chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
#     return chain

# def user_input(user_question):
#     embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001", google_api_key=GOOGLE_GEMINI_KEY)
#     new_db_files = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
#     docs = new_db_files.similarity_search(user_question, k=10)
#     chain = get_conversational_chain()
#     response = chain({"input_documents": docs, "question": user_question}, return_only_outputs=True)
#     return response["output_text"]

# @app.route("/api/question", methods=["POST"])
# def ask_question():
#     data = request.get_json()
#     question = data.get("question")
#     if not question:
#         return jsonify({"error": "No question provided"}), 400
    
#     try:
#         # Process the question and get the answer
#         answer = user_input(question)
#         return jsonify({"answer": answer})
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# if __name__ == "__main__":
#     # Preprocess the PDF when starting the server
#     if not os.path.exists("faiss_index"):
#         raw_text = get_pdf_text("lesson.pdf")
#         text_chunks = get_text_chunks(raw_text)
#         get_vector_store(text_chunks)
        
#     # Run Flask server
#     app.run(debug=True)
# import os
# 
# from flask import Flask, jsonify, request
# from flask_cors import CORS
# 
# from langchain_google_genai import GoogleGenerativeAIEmbeddings
# from langchain_community.vectorstores import FAISS
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain.chains.question_answering import load_qa_chain
# from langchain.prompts import PromptTemplate
# from PyPDF2 import PdfReader
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# 
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()
# GOOGLE_GEMINI_KEY = os.getenv("GOOGLE_GEMINI_KEY")

# # Initialize Flask App
# app = Flask(_name_)
# CORS(app)

# Global list to store generated questions

# from flask import Flask, render_template, Response, jsonify
# import cv2
# from cvzone.HandTrackingModule import HandDetector
# import numpy as np
# import google.generativeai as genai
# from PIL import Image
# import os
# import signal
# import sys

# from dotenv import load_dotenv
# from flask_cors import CORS

# load_dotenv()
# app = Flask(_name_)
# CORS(app)


import random
import numpy as np
import google.generativeai as genai
from PIL import Image
from flask import Flask, request, Response, jsonify
import cv2
from cvzone.HandTrackingModule import HandDetector
from flask_cors import CORS
from pydantic import BaseModel
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
import os
import signal
import sys
from dotenv import load_dotenv
import time
app = Flask(__name__)
CORS(app)  # Enable CORS to allow cross-origin requests

# Load API key from .env file
load_dotenv()
GOOGLE_GEMINI_KEY = os.getenv("GOOGLE_API_KEY")

UPLOAD_FOLDER = "./uploads"

current_questions = []
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(staticMode=False, maxHands=1, modelComplexity=1, detectionCon=0.7, minTrackCon=0.5)

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

prev_pos = None
canvas = None
output_text = ""  # Store the AI output globally

def getHandInfo(img):
    hands, img = detector.findHands(img, draw=False, flipType=True)
    if hands:
        hand = hands[0]
        lmList = hand["lmList"]
        fingers = detector.fingersUp(hand)
        return fingers, lmList
    else:
        return None

def draw(info, prev_pos, canvas, img):
    fingers, lmList = info
    current_pos = None
    if fingers == [0, 1, 0, 0, 0]:
        current_pos = lmList[8][0:2]
        if prev_pos is None: prev_pos = current_pos
        cv2.line(canvas, tuple(current_pos), tuple(prev_pos), (255, 0, 255), 10)
    elif fingers == [1, 0, 0, 0, 0]:
        canvas = np.zeros_like(img)
    return current_pos, canvas

def sendToAI(model, canvas, fingers):
    global output_text  # Use the global variable to store the result
    if fingers == [1, 1, 1, 1, 0]:
        pil_image = Image.fromarray(canvas)
        response = model.generate_content(["Solve this math problem", pil_image])
        output_text = response.text  # Store the AI output
        print("AI Output:", output_text)

    return ""

def gen_frames():
    global prev_pos, canvas
    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)

        if canvas is None:
            canvas = np.zeros_like(img)

        info = getHandInfo(img)
        if info:
            prev_pos, canvas = draw(info, prev_pos, canvas, img)
            sendToAI(model, canvas, info[0])

        image_combined = cv2.addWeighted(img, 0.7, canvas, 0.3, 0)
        ret, buffer = cv2.imencode('.jpg', image_combined)
        frame = buffer.tobytes()
        time.sleep(0.03)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/get_ai_output')
def get_ai_output():
    global output_text
    return jsonify({"ai_output": output_text}) 
# Models
class PDFInput(BaseModel):
    num_detailed_questions: int
    num_small_questions: int

class QuestionAnswerInput(BaseModel):
    question_number: int
    answer: str

# Core Logic for QA and Question Generation
class QAProcessor:
    def __init__(self, google_api_key, faiss_index_path="faiss_index"):
        self.google_api_key = google_api_key
        self.faiss_index_path = faiss_index_path
        self.vector_store = None
        self.raw_text = None

    def load_or_create_vector_store(self):
        if not self.vector_store:
            embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=self.google_api_key)
            if os.path.exists(self.faiss_index_path):
                print("Loading existing FAISS index...")
                self.vector_store = FAISS.load_local(self.faiss_index_path, embeddings, allow_dangerous_deserialization=True)
            else:
                text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
                chunks = text_splitter.split_text(self.raw_text)
                vector_store = FAISS.from_texts(chunks, embedding=embeddings)
                vector_store.save_local("faiss_index")
                self.vector_store = FAISS.load_local(self.faiss_index_path, embeddings, allow_dangerous_deserialization=True)

    def evaluate_answer(self, question, answer):
        self.load_or_create_vector_store()

        if not self.vector_store:
            raise RuntimeError("Vector store not initialized. Please create or load the FAISS index.")

        docs = self.vector_store.similarity_search(question)
        if not docs:
            raise ValueError("No relevant documents found for the given question.")

        context = docs[0].page_content
        context_document = Document(page_content=context)

        prompt_template = """
        Evaluate the student's answer to the question based on the provided context.

        If the answer is correct, award full marks and briefly explain why.
        If the answer is partially correct, award partial marks, explain what's missing or incorrect, and offer suggestions for improvement.
        If the answer is incorrect, give zero marks, provide the correct answer simply, and give constructive feedback.
        IMPORTANT: Always provide the marks. Marks are mandatory and should not be omitted under any circumstances.

        Be concise, friendly, and encouraging in your feedback.

        Context: {context}
        Question: {question}
        Student's Answer: {answer}

        Teacher's Feedback (including marks):
        """
        model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3, google_api_key=self.google_api_key)
        prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question", "answer"])
        chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)

        response = chain.invoke({
            "input_documents": [context_document],
            "question": question,
            "answer": answer
        }, return_only_outputs=True)

        return response["output_text"]

class QuestionGenerator:
    def __init__(self, google_api_key, model_name="gemini-pro"):
        self.model_name = model_name
        self.google_api_key = google_api_key

    def get_question_generation_chain(self, is_detailed):
        prompt_template = """
        Based on the provided context, generate a list of {marks}-mark questions that are {detailed_or_small}. The number of questions should match the {number}

        Context:\n {context}\n
        {detailed_or_small} Questions List=['question 1', 'question 2', 'question 3', ...]
        """
        detailed_or_small = "detailed (10 marks)" if is_detailed else "small (2 marks)"
        marks = 10 if is_detailed else 2

        model = ChatGoogleGenerativeAI(model=self.model_name, temperature=0.3, google_api_key=self.google_api_key)
        prompt = PromptTemplate(template=prompt_template, input_variables=["context", "detailed_or_small", "marks", "number"])
        chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
        return chain

    def generate_questions(self, context, num_detailed, num_small):
        questions = []
        context_document = Document(page_content=context)

        if num_detailed > 0:
            chain_detailed = self.get_question_generation_chain(is_detailed=True)
            detailed_response = chain_detailed.invoke({
                "input_documents": [context_document],
                "context": context,
                "detailed_or_small": "detailed",
                "marks": 10,
                "number": num_detailed
            })
            detailed_questions = detailed_response["output_text"].split('\n')
            detailed_questions = [q.split('. ', 1)[1] for q in detailed_questions if '. ' in q]
            questions.extend([(q, 10) for q in detailed_questions[:num_detailed]])

        if num_small > 0:
            chain_small = self.get_question_generation_chain(is_detailed=False)
            small_response = chain_small.invoke({
                "input_documents": [context_document],
                "context": context,
                "detailed_or_small": "small",
                "marks": 2,
                "number": num_small
            })
            small_questions = small_response["output_text"].split('\n')
            small_questions = [q.split('. ', 1)[1] for q in small_questions if '. ' in q]
            questions.extend([(q, 2) for q in small_questions[:num_small]])

        return questions

def get_pdf_text(pdf_path):
    if os.path.isfile(pdf_path):
        pdf_reader = PdfReader(pdf_path)
        return "".join([page.extract_text() for page in pdf_reader.pages])
    raise FileNotFoundError(f"No such file: '{pdf_path}'")

def generate_context(text, num_chars=10000):
    max_start = max(0, len(text) - num_chars)
    start = random.randint(0, max_start)
    return text[start:start + num_chars]

# Routes

@app.route('/generate_questions', methods=['POST'])
def generate_questions():
    try:
        print("1")
        file = request.files['pdf_file']
        print(f"Received file: {file.filename}")  # Debug line
        if file:
            pdf_path = os.path.join('uploads', file.filename)
            file.save(pdf_path)

            raw_text = get_pdf_text(pdf_path)
            context = generate_context(raw_text)
            data = request.form
            question_generator = QuestionGenerator(google_api_key=GOOGLE_GEMINI_KEY)

            questions = question_generator.generate_questions(context, int(data['num_detailed_questions']), int(data['num_small_questions']))

            if questions:
                global current_questions
                current_questions = questions  # Store the generated questions
                return jsonify({
                    'status': 'success',
                    'questions': [{'number': i+1, 'question': q[0], 'marks': q[1]} for i, q in enumerate(questions)]
                })
            else:
                return jsonify({'status': 'error', 'message': 'No questions could be generated.'}), 500
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    try:
        data = request.get_json()
        global current_questions
        if not current_questions or data['question_number'] > len(current_questions):
            return jsonify({'status': 'error', 'message': 'Invalid question number.'}), 400

        question, _ = current_questions[data['question_number'] - 1]  # Get the relevant question

        qa_processor = QAProcessor(google_api_key=GOOGLE_GEMINI_KEY)
        response = qa_processor.evaluate_answer(question, data['answer'])
        return jsonify({'status': 'success', 'response': response})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
    
def get_pdf_text(file):
    pdf_reader = PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks

def get_vector_store(text_chunks,index_path):
    
    embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001", google_api_key=GOOGLE_GEMINI_KEY)
    print("10")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    faiss_index_path="faiss_index"+ index_path
    vector_store.save_local(faiss_index_path)
    return faiss_index_path
    
def get_conversational_chain():
    prompt_template = """   
    Answer the question as detailed as possible from the provided context, make sure to provide all the details, if the answer is not in
    provided context try to relate it with context and provide answer, but don't provide the wrong answer\n\n
    Context:\n {context}?\n
    Question: \n{question}\n
    Answer:
    """

    model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3, google_api_key=GOOGLE_GEMINI_KEY)
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
    return chain

def user_input(user_question,index_path):
    embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001", google_api_key=GOOGLE_GEMINI_KEY)
    new_db_files = FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)
    docs = new_db_files.similarity_search(user_question, k=10)
    print("1")
    print(docs)
    chain = get_conversational_chain()
    response = chain({"input_documents": docs, "question": user_question}, return_only_outputs=True)
    return response["output_text"]

@app.route("/api/upload", methods=["POST"])
def upload_pdf():
    try:
        global pdf_file
        # Extract PDF file and question from the request
        pdf_file = request.files['pdf']
        question = request.form['question'] 
        
        
        pdf_path='uploads/'+ pdf_file.filename
        print(pdf_path)
    
        
        index_path="faiss_index_"+pdf_file.filename
        print(index_path)
        print(pdf_file.filename)
        if not os.path.exists(index_path):
            
            file_path = os.path.join(UPLOAD_FOLDER, pdf_file.filename)
            pdf_file.save(file_path)
            
            
            raw_text = get_pdf_text(pdf_path)
            print("^")
            text_chunks = get_text_chunks(raw_text)
            
            faiss_index_path=get_vector_store(text_chunks,index_path)
            

        
        # Send documents to chat model
        response=user_input(question,index_path=faiss_index_path)
       
        

        return jsonify({"answer": response})
    
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(port=5000,debug=True)