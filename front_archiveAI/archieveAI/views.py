from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from .models import resposta as RespostaModel
import json
import os
import google.generativeai as genai
import requests

@csrf_exempt
def sqlchat_proxy(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método não permitido'}, status=405)

    try:
        payload = json.loads(request.body.decode('utf-8'))
        pergunta = payload.get('pergunta', '').strip()
    except (json.JSONDecodeError, AttributeError):
        return JsonResponse({'error': 'Formato de requisição inválido.'}, status=400)

    if not pergunta:
        return JsonResponse({'error': 'Pergunta vazia'}, status=400)

    sqlchat_url = 'http://localhost:8000/api/chat'
    data_to_sqlchat = {'question': pergunta}

    try:
        response = requests.post(sqlchat_url, json=data_to_sqlchat)
        response.raise_for_status()

        sqlchat_data = response.json()
        sql_query = sqlchat_data.get('sql', 'Não foi possível gerar SQL.')

        # --- NOVO CÓDIGO PARA EXECUTAR A QUERY ---
        if sql_query and "SELECT" in sql_query.upper():
            with connection.cursor() as cursor:
                cursor.execute(sql_query)

                # Pega a primeira linha da resposta
                result = cursor.fetchone() 

                # Converte o resultado para string
                result_str = str(result[0]) if result else "Nenhum resultado encontrado."

                return JsonResponse({'resposta': result_str, 'source': 'bd'})
        else:
            return JsonResponse({'resposta': "O SQLChat não gerou uma consulta válida.", 'source': 'sqlchat_error'})

    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': f'Erro na comunicação com o SQLChat: {e}'}, status=500)

def home(request):
    return render(request, "busca/home.html")

def resposta(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Use POST'}, status=400)

    try:
        payload = json.loads(request.body.decode('utf-8'))
        pergunta = payload.get('pergunta', '').strip()
    except Exception:
        pergunta = request.POST.get('pergunta', '').strip()

    if not pergunta:
        return JsonResponse({'error': 'Pergunta vazia'}, status=400)

    found = RespostaModel.objects.filter(pergunta__icontains=pergunta).first()
    if not found:
        found = RespostaModel.objects.filter(resposta__icontains=pergunta).first()

    if found:
        return JsonResponse({'resposta': found.resposta, 'source': 'db'})

    answer = call_ia(pergunta)

    novo = RespostaModel(pergunta=pergunta, resposta=answer)
    novo.save()

    return JsonResponse({'resposta': answer, 'source': 'ai_saved'})

def call_ia(pergunta: str) -> str:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return "[ERRO] GEMINI_API_KEY não configurada"

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(pergunta)
        return response.text
    except Exception as e:
        return f"[ERRO AO CONSULTAR GEMINI] {e}"