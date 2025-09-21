from django.db import models

class resposta(models.Model):
    pergunta = models.TextField(help_text='Texto da pergunta enviada pelo usuário')
    resposta = models.TextField(help_text='Resposta encontrada ou gerada pela IA')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.pergunta[:50]
