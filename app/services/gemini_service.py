import os
import time
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from dotenv import load_dotenv

load_dotenv()

class GeminiService:
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        self.client = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0, google_api_key=api_key)

        self.db = SQLDatabase.from_uri("mysql+pymysql://root:ifsp@localhost/uni1500_negocio")

        self.toolkit = SQLDatabaseToolkit(db=self.db, llm=self.client)

        self.agent_executor = create_sql_agent(
            llm=self.client,
            toolkit=self.toolkit,
            verbose=True
        )

    def get_table_info(self):

        try:
            query = "SHOW TABLES"
            tables = self.db.run(query)
            table_list = [table[0] for table in tables]
            return ", ".join(table_list)
        except Exception as e:
            print(f"Erro ao recuperar informações das tabelas: {str(e)}")
            return "Erro ao recuperar tabelas"

    def execute_prompt_sql(self, prompt):
        try:
            full_prompt = f"""
                            Todas as respostas devem ser em Português. 

                            Pergunta atual:
                            {prompt}
                            """
            return self.agent_executor.run(full_prompt)
        except Exception as e:
            print(f"Erro ao executar a consulta: {str(e)}")
            return None

    def execute_prompt_normal(self, prompt, historico=None):
        try:
            if historico:
                full_prompt = f"""
                Contexto (histórico de conversas anteriores):
                {historico}

                Pergunta atual:
                {prompt}
                """
            else:
                full_prompt = prompt
            return self.client.invoke(full_prompt.strip()).content
        except Exception as e:
            print(f"Erro ao executar a consulta: {str(e)}")
            return None

    def should_use_db(self, prompt):

        table_info = self.get_table_info()
        table_info = table_info.strip('[]').replace(',', '').replace(' ', '')
        table_info = table_info.split("'")
        table_info = [item.strip('()') for item in table_info if item.strip('()')]

        full_prompt = f"""
        Tabelas do banco de dados:
        {table_info}

        O seguinte prompt parece estar pedindo informações de interações passadas ou dados que possam estar em alguma tabela? Caso ache que sim, digite SIM! SIM! ou NÃO! NÃO! se não for. Prompt: '{prompt}'
        """

        response = self.execute_prompt_normal(full_prompt.strip())

        return "sim" in response.lower()

    def process_message(self, prompt, historico):

        if self.should_use_db(prompt):
            resposta_db = self.execute_prompt_sql(prompt)
            if resposta_db:
                print(f"Resposta da consulta ao banco de dados: {resposta_db}")
                return resposta_db

        resposta_llm = self.execute_prompt_normal(prompt, historico)
        return resposta_llm


