from django import template
from django.contrib.auth.models import Group

register = template.Library()

@register.filter(name='in_group')
def in_group(user, group_name):
    """Filters on a User instance, takes as argument the name of a group, returns
    true if the user belongs to the group.
    """
    group = Group.objects.get(name=group_name)
    return group in user.groups.all()
