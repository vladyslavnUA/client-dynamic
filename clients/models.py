from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.CharField(max_length=100, blank=True)
    bio = models.CharField(max_length=3000, blank=True)
    role = models.CharField(max_length=100, blank=True)
    fb_page_id = models.CharField(max_length=200, blank=True)
    fb_page_token = models.CharField(max_length=30000, blank=True)

    def __str__(self):  # __unicode__ for Python 2
        return self.user.username

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

class Client(models.Model):
    name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(max_length=350, blank=True)
    address = models.CharField(max_length=350, blank=True)

    def __str__(self):
        return self.name