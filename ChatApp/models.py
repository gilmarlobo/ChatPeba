from django.db import models

class Mensagem(models.Model):
    autor = models.CharField(max_length=100)
    conteudo = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.autor}: {self.conteudo[:20]}"
