import os
import time
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from dotenv import load_dotenv
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END

load_dotenv()

class AgentState(TypedDict):
    prompt: str
    historico: Annotated[str, None]
    enhanced_prompt: Annotated[str, None]
    is_sql: Annotated[bool, None]
    sql_result: Annotated[str, None]
    normal_result: Annotated[str, None]

class GeminiService:
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        self.client = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.2, google_api_key=api_key)
        self.db = SQLDatabase.from_uri("mysql+pymysql://root:ifsp@localhost/uni1500_negocio")
        self.toolkit = SQLDatabaseToolkit(db=self.db, llm=self.client)
        self.agent_executor = create_sql_agent(llm=self.client, toolkit=self.toolkit, verbose=True)

    def check_sql(self, state: AgentState) -> AgentState:
        table_info = self.db.get_table_info()

        prompt_check = (f"As Respostas devem ser obrigatóriamente em português.\n"
                        f"------------------------------------------\n"
                        f"Histórico (Contexto): {state['historico']}\n"
                        f"------------------------------------------\n"
                        f"Tables: {table_info}. \n"
                        f"------------------------------------------\n"
                        f"O prompt a baixo com base no histórico de conversa, nas tabelas do banco. Este prompt a seguir deseja realizar uma consulta no meu banco?\n"
                        f"1. Caso sim, digite SIM! SIM!\n"
                        f"2. Caso não, digite NÃO! NÃO!\n"
                        f"------------------------------------------\n"
                        f"Prompt: {state['prompt']}")
        response = self.client.invoke(prompt_check).content
        state["is_sql"] = "sim" in response.lower()
        return state

    def enhance_prompt(self, state: AgentState) -> AgentState:
        table_info = self.db.get_table_info()

        prompt_check = (f"As Respostas devem ser obrigatóriamente em português.\n"
                        f"------------------------------------------\n"
                        f"Aqui está o histórico dessa conversa somente para seu contexto:\n"
                        f"Histórico: {state['historico']}\n"
                        f"------------------------------------------\n"
                        f"Apenas observe o banco:\n"
                        f"Tables: {table_info}. \n"
                        f"------------------------------------------\n"
                        f"Esse Prompt será enviado a uma LLM que trocará a linguagem natural do prompt para um SQL.\n"
                        f"1. Entenda o contexto."
                        f"2. Entenda o que o prompt realmente deseja encontrar."
                        f"3. Retorne o prompt reformulado ainda em linguagem natural considerando o contexto."
                        f"------------------------------------------\n"
                        f"Retorne em linguagem natural a melhor versão deste "
                        f"Prompt: {state['prompt']}")

        # Chama o agente LLM para melhorar o prompt
        enhanced_prompt = self.client.invoke(prompt_check).content

        print("-------------------Original------------------------------")
        print(state['prompt'])
        print("-----------------PROCESSADO--------------------------------")
        print(enhanced_prompt)
        print("-------------------------------------------------")

        # Atualiza o estado com o prompt melhorado
        state["enhanced_prompt"] = enhanced_prompt.strip()

        return state

    def execute_sql(self, state: AgentState) -> AgentState:

        prompt_check = (f"As Respostas devem ser obrigatóriamente em português.\n"
                        f"{state["enhanced_prompt"]}")

        try:
            query_result = self.agent_executor.run(prompt_check)
            state["sql_result"] = query_result
        except:
            state["sql_result"] = "Ops... Não consegui realizar a pesquisa! Por favor me mande novamente a pergunta reformulada. 😁"


        return state

    def execute_normal(self, state: AgentState) -> AgentState:
        prompt_check = (f"As Respostas devem ser obrigatóriamente em português.\n"
                        f"------------------------------------------\n"
                        f"Aqui está o histórico dessa conversa somente para seu contexto:\n"
                        f"Histórico: {state['historico']}\n"
                        f"------------------------------------------\n"
                        f"Responda, em português, de maneira mais correta possível o prompt do usuário.\n"
                        f"------------------------------------------\n"
                        f"Prompt: {state['prompt']}\n")

        normal_result = self.client.invoke(prompt_check).content
        state["normal_result"] = normal_result
        return state

    def process_message(self, prompt, historico=None):
        state = AgentState(prompt=prompt, historico=historico, enhanced_prompt=None, is_sql=None, sql_result=None, normal_result=None)

        # Cria o gráfico de agentes
        graph = StateGraph(AgentState)

        # Define o ponto de entrada para o gráfico
        graph.set_entry_point("check_sql")

        # Adiciona os nós ao gráfico
        graph.add_node("check_sql", self.check_sql)
        graph.add_node("enhance_prompt", self.enhance_prompt)
        graph.add_node("execute_sql", self.execute_sql)
        graph.add_node("execute_normal", self.execute_normal)

        # Define o fluxo condicional do gráfico
        def routing_logic(state: AgentState):
            return "enhance_prompt" if state["is_sql"] else "execute_normal"

        graph.add_conditional_edges("check_sql", routing_logic)
        graph.add_edge("enhance_prompt", "execute_sql")
        graph.add_edge("execute_sql", END)
        graph.add_edge("execute_normal", END)

        # Compila e executa o gráfico
        agent_app = graph.compile()
        final_state = agent_app.invoke(state)

        # Retorna o resultado final
        return final_state["sql_result"] or final_state["normal_result"]
