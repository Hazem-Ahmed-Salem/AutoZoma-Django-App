from .models import Profile ,Location
from main.models import Listing
from django.contrib.auth.models import User
from django.db.models.signals import (
    post_save,
    post_delete
    )
from django.dispatch import receiver
from autozoma.settings import BASE_DIR
import shutil

@receiver(post_save,sender=User)
def create_user_profile(sender , instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance,photo='user_0/12.png')


@receiver(post_save , sender=Profile)
def create_profile_location (sender , instance , created ,**kwargs):
    if created:
        print(instance.__str__())
        Profile_Location=Location.objects.create(user=instance.user)
        instance.location=Profile_Location
        instance.save()

@receiver(post_delete , sender=Profile)
def delete_Location(sender , instance , **kwargs ):
    if instance.location:
        instance.location.delete()
    if instance.photo:
        try:
            shutil.rmtree(f'{BASE_DIR}/media/user_{instance.user.id}/')
        except FileNotFoundError :
            return
        except Exception as e:
            print(e)


@receiver(post_delete , sender=Listing)
def delete_Location(sender , instance , **kwargs ):
    if instance.location:
        instance.location.delete()