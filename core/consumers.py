import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Message, Match, Utilisateur

#  Websocket pour la messagerie en temps réel - MentorLink IFRI
class ChatConsumer(AsyncWebsocketConsumer):

    # Connexion d'un utilisateur à la salle de chat du match
    async def connect(self):
        self.match_id = self.scope['url_route']['kwargs']['match_id']  
        self.room_group_name = f"chat_{self.match_id}"
        self.notif_group_name = f"notifications_{self.match_id}"  #  groupe pour notifications

        # Rejoindre le groupe de la conversation
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        #  Rejoindre aussi le groupe des notifications
        await self.channel_layer.group_add(
            self.notif_group_name,
            self.channel_name
        )

        await self.accept()

    # Déconnexion d'un utilisateur
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        # Quitter aussi le groupe notifications
        await self.channel_layer.group_discard(
            self.notif_group_name,
            self.channel_name
        )

    # Réception d'un message depuis le frontend
    async def receive(self, text_data):
        data = json.loads(text_data)
        contenu = data['contenu']
        expediteur_id = data['expediteur_id']

        # Sauvegarder le message en base de données
        message = await self.sauvegarder_message(expediteur_id, contenu)

        # Diffuser le message à tous les membres du groupe en temps réel
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': contenu,
                'expediteur_id': expediteur_id,
                'message_id': message.id
            }
        )
        
        #  Envoyer une notification séparée (alerte, pas le message complet)
        await self.envoyer_notification(expediteur_id, contenu)

    # Envoi du message au frontend
    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'new_message',  
            'message': event['message'],
            'expediteur_id': event['expediteur_id'],
            'message_id': event['message_id']
        }))

    # Méthode pour envoyer une notification
    async def envoyer_notification(self, expediteur_id, contenu):
        # Récupérer le nom de l'expéditeur
        expediteur_nom = await self.get_expediteur_nom(expediteur_id)
        
        # Envoyer une notification au groupe (alerte, pas le message complet)
        await self.channel_layer.group_send(
            self.notif_group_name,
            {
                'type': 'notification_alerte',
                'message': f"📬 Nouveau message de {expediteur_nom}",
                'expediteur_id': expediteur_id,
                'match_id': self.match_id,
                'apercu': contenu[:50] + "..." if len(contenu) > 50 else contenu
            }
        )

    #  : Envoi de la notification au frontend
    async def notification_alerte(self, event):
        # Envoie une notification distincte (pas dans la conversation)
        await self.send(text_data=json.dumps({
            'type': 'notification',  # Type différent de 'new_message'
            'titre': 'Nouveau message',
            'message': event['message'],
            'expediteur_id': event['expediteur_id'],
            'match_id': event['match_id'],
            'apercu': event['apercu']
        }))

    # Sauvegarde du message en base PostgreSQL
    @database_sync_to_async
    def sauvegarder_message(self, expediteur_id, contenu):
        match = Match.objects.get(id=self.match_id)
        expediteur = Utilisateur.objects.get(id=expediteur_id)
        return Message.objects.create(
            match=match,
            expediteur=expediteur,
            contenu=contenu
        )
    
    #  Récupérer le nom de l'expéditeur
    @database_sync_to_async
    def get_expediteur_nom(self, expediteur_id):
        try:
            utilisateur = Utilisateur.objects.get(id=expediteur_id)
            return f"{utilisateur.prenom} {utilisateur.nom}"  # Adapte selon tes champs
        except Utilisateur.DoesNotExist:
            return "Un utilisateur"