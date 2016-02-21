from django.contrib.auth.models import User

def is_superauthor(user):
	check = user.groups.filter(name='superauthor').exists()
	return check