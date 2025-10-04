from django.urls import path
from .views import MensagemListView

urlpatterns = [
    path("mensagens/", MensagemListView.as_view(), name="mensagem-list"),
]
