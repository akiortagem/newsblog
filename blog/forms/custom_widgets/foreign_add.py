from django.template.loader import render_to_string
import django.forms as forms

class SelectWithPlus(forms.Select):

    def render(self, name, *args, **kwargs):
        html = super(SelectWithPlus, self).render(name, *args, **kwargs)
        plus = render_to_string("plus.html", {'field': name})
        return html+plus
