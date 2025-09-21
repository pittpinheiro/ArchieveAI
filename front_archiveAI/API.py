import os
import google.generativeai as genai

api_key = "AIzaSyD-RPaFTss4hzCYdH4BiUbYhlujfwjfTvE"
if not api_key:
    print("[ERRO] Variável de ambiente GEMINI_API_KEY não está configurada.")
else:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content("Qual a capital do Brasil?")

        print("Resposta da API:")
        print(response.text)

    except Exception as e:
        print(f"\n[ERRO GERAL] Ocorreu um erro inesperado: {e}")