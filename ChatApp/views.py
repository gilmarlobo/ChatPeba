from rest_framework import generics
from .models import Mensagem
from .serializers import MensagemSerializer

# Lista todas mensagens (histórico)
class MensagemListView(generics.ListAPIView):
    queryset = Mensagem.objects.all().order_by("timestamp")
    serializer_class = MensagemSerializer
