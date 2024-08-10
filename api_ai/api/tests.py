from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import User, Post, Comment
from datetime import date, datetime, timedelta

class AccountTests(APITestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.user_data = {'username': 'testuser', 'password': '1234', 'email': 'test@test.test'}
        self.user = User.objects.create(**self.user_data)
        self.client.force_authenticate(user=self.user)


    def test_create_account(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('user')
        data = {'username': 'user', 'password': 'passowrd', 'email': 'user@email.com'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(id=response.data.get('id'))
        self.assertEqual(user.username, data['username'])


    def test_post_comment_brakedown_create(self):
        url = reverse('post')
        data = {'title': 'title1', 'content': 'somecontent offencive'}
        response = self.client.post(url, data, format='json')
        post = Post.objects.get(title=data['title'])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(post.content, data['content'])
        comment_qty = 10
        for n in range(comment_qty):
            self.client.post(reverse('comment'), {'content': f'somecontent{n}', 'post_id': post.id}, format='json')
        self.assertEqual(len(Comment.objects.all()), comment_qty)
        now = date.today()
        brakedown = self.client.get(reverse('brakedown')+
            f'?date_from={((now - timedelta(days=1)).strftime('%Y-%m-%d'))}&date_to={(now+timedelta(days=1)).strftime('%Y-%m-%d')}', format='json')
        self.assertEqual(len(brakedown.data), 3)
        self.assertEqual(brakedown.status_code, status.HTTP_200_OK)

    
