from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
#
def user_directory_path(instance, filename):
    return 'user_{0}/profile/{1}'.format(instance.user.id, filename)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=20, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(null=True, upload_to = user_directory_path, default = 'default_profile_pic.jpg', blank=True)
    
    @classmethod
    def create(cls, name, nickname='', description='', image=None):
        profile = cls(
            user=User.objects.get_or_create(username=name),
            nickname=nickname,
            description=description,
            image=image
        )
        return profile
    
    def __str__(self):
        return '{0} owns profile'.format(
            self.user.username,
        )

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
