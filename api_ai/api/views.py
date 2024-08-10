from django.shortcuts import render
from rest_framework import generics
from .models import *
from .serializers import *
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.status import HTTP_200_OK
from django.db.models import Q
from datetime import datetime, timedelta


@csrf_exempt
@api_view(['POST'])
@permission_classes((AllowAny,))
def token(request):
    username = request.data.get('username')
    password = request.data.get('password')
    if username is None or password is None:
        return Response({'error': "name or password is empty"})
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'invalid credentials'})
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key}, status=HTTP_200_OK)

@api_view(['GET'])
@permission_classes((AllowAny,))
def daily_brakedown(request):
    date_from =request.GET.get('date_from')
    date_from = datetime.strptime(date_from, '%Y-%m-%d')
    date_to = request.GET.get('date_to')
    date_to = datetime.strptime(date_to, '%Y-%m-%d')+timedelta(days=1)
    comments = Comment.objects.filter(Q(created_at__gte=date_from) & Q(created_at__lte=date_to))
    resp = {}
    cur_date = date_from
    while cur_date < date_to:
        resp[str(cur_date.date())]={
            'created':len(comments.filter(Q(created_at__gte=cur_date)&Q(created_at__lt=cur_date+timedelta(days=1)))),
            'blocked': len(comments.filter(Q(is_blocked=1)&Q(created_at__gte=cur_date)&Q(created_at__lt=cur_date+timedelta(days=1)))),
        }
        cur_date += timedelta(days=1)
    return Response(resp, status=HTTP_200_OK)


class PostCreateListApiView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,]
    def perform_create(self, serializer):
        serializer.save(owner_id=self.request.user)

class CommentCreateListApiView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,]
    def perform_create(self, serializer):
        serializer.save(owner_id=self.request.user)

class UserCreateApiView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer


class PostRetrieveUpdateDestroyApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,]
    def perform_update(self, serializer):
        serializer.save(owner_id=self.request.user)

class CommentRetrieveUpdateDestroyApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,]
    def perform_update(self, serializer):
        serializer.save(owner_id=self.request.user)




