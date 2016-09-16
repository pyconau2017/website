from django import template
from django.contrib.staticfiles.templatetags import staticfiles

register = template.Library()

@register.assignment_tag()
def classname(ob):
    return ob.__class__.__name__

@register.simple_tag(takes_context=True)
def can_manage(context, proposal):
    return proposal_permission(context, "manage", proposal)

@register.simple_tag(takes_context=True)
def can_review(context, proposal):
    return proposal_permission(context, "review", proposal)

def proposal_permission(context, permname, proposal):
    slug = proposal.kind.section.slug
    perm = "reviews.can_%s_%s" % (permname, slug)
    return context.request.user.has_perm(perm)


# {% load statictags %}{% static 'lca2017/images/svgs/illustrations/' %}{{ illustration }}

@register.simple_tag(takes_context=False)
def illustration(name):
    return staticfiles.static('lca2017/images/svgs/illustrations/') + name
