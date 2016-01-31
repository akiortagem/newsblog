from django import template
register = template.Library()

@register.filter(name='addcss')
def addcss(field, css):
	"""
	register a filter so it can be used like so {{ field|addcss:"classname" }}
	"""
	return field.as_widget(attrs={"class":css})

@register.filter(name='get_range')
def get_range(value):
	return range(value)
	
@register.filter(name='tablecss')
def tablecss(table, css):
	"""
	register a filter for a table
	"""
	table.Meta.attrs={"class":css}
	return table
