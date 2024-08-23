import openai

# Configurar a chave da API do ChatGPT
openai.api_key = 'sua_chave_api_chatgpt'

def ask_chatgpt(question):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=question,
        max_tokens=150
    )
    return response.choices[0].text.strip()
