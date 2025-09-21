import os
import google.generativeai as genai

api_key = "AIzaSyBcCGVSujOmhF829Ps7GXGiYyWjWImuLzM"
if not api_key:
    print("[ERRO] Variável de ambiente GEMINI_API_KEY não está configurada.")
else:
    try:
        print("Configurando a API do Gemini...")
        genai.configure(api_key=api_key)
        
        # Escolha o modelo que você quer usar
        model = genai.GenerativeModel('gemini-1.5-flash')

        print("Enviando requisição de teste para a API do Gemini...")
        pergunta = "Qual a capital do Brasil?"
        response = model.generate_content(pergunta)
        
        print("\n--- RESPOSTA DA API ---")
        print(response.text)
        
    except Exception as e:
        print(f"\n[ERRO GERAL] Ocorreu um erro inesperado: {e}")