from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import Utilisateur, OffreDemande, Conversation, Message
from .serializers import *

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({'token': str(refresh.access_token), 'userId': user.id}, status=201)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    user = authenticate(username=email, password=password)
    if user:
        refresh = RefreshToken.for_user(user)
        return Response({'token': str(refresh.access_token), 'userId': user.id})
    return Response({'error': 'Identifiants incorrects'}, status=401)

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def profil(request):
    if request.method == 'GET':
        return Response(UtilisateurSerializer(request.user).data)
    serializer = UtilisateurSerializer(request.user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def utilisateurs(request):
    users = Utilisateur.objects.exclude(id=request.user.id)
    return Response(UtilisateurSerializer(users, many=True).data)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def offres(request):
    if request.method == 'GET':
        data = OffreDemande.objects.filter(utilisateur=request.user)
        return Response(OffreDemandeSerializer(data, many=True).data)
    serializer = OffreDemandeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(utilisateur=request.user)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def messages(request, conv_id):
    try:
        conv = Conversation.objects.get(id=conv_id, participants=request.user)
    except Conversation.DoesNotExist:
        return Response({'error': 'Conversation introuvable'}, status=404)
    if request.method == 'GET':
        msgs = Message.objects.filter(conversation=conv).order_by('date_envoi')
        return Response(MessageSerializer(msgs, many=True).data)
    msg = Message.objects.create(
        conversation=conv,
        expediteur=request.user,
        contenu=request.data.get('contenu', '')
    )
    return Response(MessageSerializer(msg).data, status=201)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def creer_conversation(request):
    other_id = request.data.get('utilisateur_id')
    try:
        other = Utilisateur.objects.get(id=other_id)
    except Utilisateur.DoesNotExist:
        return Response({'error': 'Utilisateur introuvable'}, status=404)
    conv = Conversation.objects.filter(participants=request.user).filter(participants=other).first()
    if not conv:
        conv = Conversation.objects.create()
        conv.participants.add(request.user, other)
    return Response({'conv_id': conv.id})