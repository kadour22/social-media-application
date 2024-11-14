from django.db.models.signals import post_save
from .models import User , Account


def create_user_account(sender , instance , created , **kwargs) :
       if created :
              account = Account.objects.create(user=instance)
              account.save()

post_save.connect(create_user_account , sender=User)