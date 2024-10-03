from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv('gemini.env')


app = Flask(__name__)
CORS(app)

# Configurar a chave API do Google Gemini
GOOGLE_GEMINI_API_KEY = os.getenv('GOOGLE_GEMINI_API_KEY')
genai.configure(api_key=GOOGLE_GEMINI_API_KEY)

# Função para gerar respostas usando a API do Google Gemini
def gerar_resposta(pergunta):
    prompt = (
        f"Você é um especialista em Veganismo. Responda à seguinte pergunta de forma clara e concisa: {pergunta}"
    )
    
    response = genai.GenerativeModel("gemini-1.5-flash-latest").generate_content(prompt)

    if response and response.text:
        return response.text
    else:
        return "Desculpe, não consegui encontrar uma resposta para isso."

# Rota para receber perguntas e retornar respostas
@app.route('/faq', methods=['POST'])
def faq():
    dados_usuario = request.json
    pergunta = dados_usuario['pergunta']
    
    resposta = gerar_resposta(pergunta)
    return jsonify({"resposta": resposta})

if __name__ == '__main__':
    app.run(debug=True)

# Rota de boas-vindas
@app.route('/')
def welcome():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)