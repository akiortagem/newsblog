from django import template
from django.contrib.auth.models import User
register = template.Library()

@register.filter(name='is_superuser')
def is_superuser(user):
  if isinstance(user, User):
    if user.groups.filter(name='superuser').exists():
      return True
    else:
      return False
  else :
    return False

@register.filter(name='is_superauthor')
def is_superauthor(user):
  if isinstance(user, User):
    if user.groups.filter(name='superauthor').exists():
      return True
    else:
      return False
  else :
    return False