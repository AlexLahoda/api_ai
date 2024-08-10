from django.urls import path
from .views import *

urlpatterns = [
    path('post/', PostCreateListApiView.as_view(), name='post'),
    path('post/<pk>/', PostRetrieveUpdateDestroyApiView.as_view()),
    path('comment/', CommentCreateListApiView.as_view(), name='comment'),
    path('comment/<pk>/', CommentRetrieveUpdateDestroyApiView.as_view()),
    path('user/', UserCreateApiView.as_view(), name='user'),
    path('token/', token, name='token'), 
    path('comments-daily-brakedown', daily_brakedown, name='brakedown')
]