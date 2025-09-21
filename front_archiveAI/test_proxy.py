import requests
import json

# URL da sua view de proxy
url = 'http://127.0.0.1:8000/sqlchat/'

# Dados que seriam enviados pelo front-end
payload = {'pergunta': 'Quantos livros existem na minha biblioteca?'}

try:
    # Envia a requisição POST para a sua view
    response = requests.post(url, json=payload)

    # Imprime o status da resposta e o corpo da resposta
    print(f"Status da Resposta: {response.status_code}")
    print("Corpo da Resposta:")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))

except requests.exceptions.RequestException as e:
    print(f"Ocorreu um erro na requisição: {e}")