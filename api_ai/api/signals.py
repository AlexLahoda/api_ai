from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Comment, Post
from .tasks import respond_to_comment, blocker

@receiver(post_save, sender=Comment)
def comment_created(sender, instance, **kwargs):
    if kwargs.get('created', False):
        time = instance.post_id.owner_id.resp_timeout
        respond_to_comment.apply_async((instance.id,),countdown=time)

@receiver(post_save, sender=Post)
def post_created(sender, instance, **kwargs):
    if kwargs.get('created', False):
        blocker.delay(instance.id)