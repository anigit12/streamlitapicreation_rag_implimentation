from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os
from dotenv import load_dotenv
load_dotenv()
class Model:
    @staticmethod
    def gemini_chat():
        model_chat=ChatGoogleGenerativeAI(
            model='gemini-1.5-flash',
            verbose=True,
            temperature=0.7,
            google_api_key=os.environ.get('GOOGLE_API_KEY')
        )
        return model_chat
    @staticmethod
    def gemini_embed():
        model_embed=GoogleGenerativeAIEmbeddings(
            model='models/text-embedding-004',
            google_api_key=os.environ.get('GOOGLE_API_KEY')
        )
        return model_embed