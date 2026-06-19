from dotenv import load_dotenv
from langchain_google_genai import (
    ChatGoogleGenerativeAI
)


load_dotenv()

llm = ChatGoogleGenerativeAI(
    model = "gemini-2.5-flash"
)


response = llm.invoke(
"""
History:

User: What is the loan amount?
AI: The loan amount is INR 25,00,000

Question:
Who approved it?

Rewrite the question only.
Do not answer.
"""
)

print(response.content)