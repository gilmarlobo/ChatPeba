import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.sala_nome = self.scope['url_route']['kwargs']['sala_nome']
        self.room_group_name = f"chat_{self.sala_nome}"

        # Entra no grupo da sala
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        autor = data['autor']
        conteudo = data['conteudo']

        # Salva no banco
        await self.salvar_mensagem(autor, conteudo)

        # Envia pra todos na sala
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'autor': autor,
                'conteudo': conteudo,
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'autor': event['autor'],
            'conteudo': event['conteudo'],
        }))

    @sync_to_async
    def salvar_mensagem(self, autor, conteudo):
        # IMPORTAÇÃO dentro do método evita o erro "Apps aren't loaded yet"
        from .models import Mensagem
        Mensagem.objects.create(autor=autor, conteudo=conteudo)
