
import os
import random
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
import google.generativeai as genai
from dotenv import load_dotenv
import uvicorn

app = FastAPI()

load_dotenv()
GOOGLE_GEMINI_KEY = os.getenv("GOOGLE_API_KEY")

# Global list to store generated questions and their marks
current_questions = []

class PDFInput(BaseModel):
    pdf_path: str
    num_detailed_questions: int
    num_small_questions: int

class QuestionAnswerInput(BaseModel):
    question_number: int
    answer: str

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


@app.post('/generate_questions')
async def generate_questions(pdf_input: PDFInput):
    global current_questions
    try:
        raw_text = get_pdf_text(pdf_input.pdf_path)
        context = generate_context(raw_text)
        question_generator = QuestionGenerator(google_api_key=GOOGLE_GEMINI_KEY)

        questions = question_generator.generate_questions(context, pdf_input.num_detailed_questions, pdf_input.num_small_questions)

        if questions:
            current_questions = questions  # Store the generated questions
            return {
                'status': 'success',
                'questions': [{'number': i+1, 'question': q[0], 'marks': q[1]} for i, q in enumerate(questions)]
            }
        else:
            raise HTTPException(status_code=500, detail="No questions could be generated.")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post('/submit_answer')
async def submit_answer(answer_input: QuestionAnswerInput):
    global current_questions
    try:
        if not current_questions or answer_input.question_number > len(current_questions):
            raise HTTPException(status_code=400, detail="Invalid question number.")

        question, _ = current_questions[answer_input.question_number - 1]  # Get the relevant question

        qa_processor = QAProcessor(google_api_key=GOOGLE_GEMINI_KEY)
        response = qa_processor.evaluate_answer(question, answer_input.answer)
        return {
            'status': 'success',
            'response': response
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

