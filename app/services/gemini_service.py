import os
import time
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

class GeminiService:
    def __init__(self):
        api_key = os.environ.get('GOOGLE_API_KEY')
        self.client = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0, google_api_key=api_key)

    def generate_response_with_retry(self, messages, max_retries=5):
        retries = 0
        while retries < max_retries:
            try:
                return self.client.invoke(messages).content
            except Exception as e:  # Captura uma exceção genérica
                wait_time = 2 ** retries  # Exponential backoff
                print(f"Erro: {str(e)}. Retentando em {wait_time} segundos.")
                time.sleep(wait_time)
                retries += 1
        raise Exception("O servico Gemini falhou apos multiplas tentativas.")