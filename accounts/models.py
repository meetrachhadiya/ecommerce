from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from accounts.managers import UserManager
from base.utils import send_activation_email
import uuid
from base.models import BaseModel
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy as _

#create model here

class User(AbstractUser):
    username = None
    first_name = models.CharField(_("first name"), max_length=150, blank=True, null=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True, null=True)
    email = models.EmailField(primary_key=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    user_bio = models.TextField(null=True, blank=True)
    user_image = models.ImageField(upload_to="profile", null=True, blank=True)
    email_token = models.CharField(max_length=100, null=True, blank=True)
    is_email_verified = models.BooleanField(default=False)
    reset_password_token = models.UUIDField(default=None , null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = 'profile'

    def __str__(self):
        return self.email
    
    def delete(self, *args, **kwargs):
        if self.user_image:
            self.user_image.delete()
        super(User, self).delete()

@receiver(post_save, sender=User)   
def send_email_token(instance, created, *args, **kwargs):
    try:
        if created:
            email_token = str(uuid.uuid4())
            instance.email_token = email_token
            send_activation_email(instance.email, email_token)
            instance.save()

    except Exception as e:
        print(e)

class Address(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses")
    name = models.CharField(max_length=200)
    phone_number = models.IntegerField()
    address = models.TextField()
    pincode = models.IntegerField()
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return (self.address)
    