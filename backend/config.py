from langchain_groq import ChatGroq
import os

from dotenv import load_dotenv
load_dotenv()


def get_llm():
    llm = ChatGroq(model="llama-3.1-8b-instant")
    return llm