from celery import shared_task
from django.utils import timezone
from .models import Comment, Post

from django.db import connection
from django.db import close_old_connections

import google.generativeai as genai
from google.api_core.exceptions import FailedPrecondition

genai.configure(api_key="api")

model = genai.GenerativeModel('gemini-1.5-flash')

def is_offencive(text: str):
    try:
        return bool(int(model.generate_content(f"Is this text have offencive content(return 1 if True or 0 if False): {text}").text))
    except FailedPrecondition as e:
        if text.find('offencive') != -1:
            return True
    return False

@shared_task
def respond_to_comment(comment_id):
    close_old_connections()
    comment = Comment.objects.get(id=comment_id)
    try:
        if comment.response_text is None:
            comment.response_text = model.generate_content(f"Comment is written to this post: {comment.post_id.content}; write an answer from the posts author name; comments content: {comment.content}").text
            comment.responded_at = timezone.now()
            comment.save()
    except FailedPrecondition as e:
        comment.response_text = "Not generated answer"
        comment.responded_at = timezone.now()
        comment.save()
    finally:
        if is_offencive(comment.content):
            comment.is_blocked = True
            comment.save()
        connection.close()

@shared_task
def blocker(post_id):
    close_old_connections()
    try:
        post = Post.objects.get(id=post_id)
        if is_offencive(post.content):
            post.is_blocked = True
            post.save()
    except Post.DoesNotExist:
        print('not exists')
    finally:
        connection.close()




    
