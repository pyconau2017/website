from django import template
register = template.Library()

@register.assignment_tag()
def classname(ob):
    return ob.__class__.__name__
