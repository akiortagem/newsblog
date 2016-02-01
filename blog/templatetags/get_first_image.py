from django import template
register = template.Library()

@register.filter(name='get_first_image')
def get_first_image(gallery):
	return gallery.images.all()[0].image