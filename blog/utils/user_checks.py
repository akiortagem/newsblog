from django.contrib.auth.models import User

def is_superauthor(user):
	check = request.user.groups.filter(name='superauthor').exists()
	return check