from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.dispatch import receiver
from django.db.models.signals import post_save


# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    phone_number = models.CharField(max_length = 10, blank=True)
    adress = models.CharField(max_length = 150, blank=True)
    city = models.CharField(max_length = 20, blank=True)
    country = models.CharField(max_length = 20, blank=True)
    image = models.ImageField(upload_to="images/users/", default="images/users/default.jpg")

    def __str__(self):
        return self.user_name()
    
    def user_name(self):
        return self.user.first_name + ' ' +self.user.last_name

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'

# Otomatik olarak profil oluşturma...
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)



