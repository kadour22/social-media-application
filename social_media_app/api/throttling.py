from datetime import date
from rest_framework.throttling import BaseThrottle
from .models import PrivateG


class CreatingPrivateGroupThrottle(BaseThrottle) :

       def allow_request(self, request, view):
             
              activate_user = request.user.accounts
              today = date.today()
              p = PrivateG.objects.filter(owner=activate_user , created_at__date=today)
             
              if p :
                     return False
              
              return True
