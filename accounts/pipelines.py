from django.shortcuts import redirect
from django.contrib.auth.models import User, Group
from social_core.pipeline.partial import partial

# partial says "we may interrupt, but we will come back here again"
@partial
def pick_group(strategy, backend, request, details, *args, **kwargs):
    #user_group session in settings.py and updated from views
    user_group = strategy.session_get('user_group', None)
    if not user_group:
        #collect user_group from view, session set to limit choosegroup view conditionally
        request.session['user_group'] = 'temp_value'
        return redirect("accounts:choosegroup")
    user = User.objects.get(email=kwargs['uid'])
    group = Group.objects.get(name=user_group)
    group.user_set.add(user)
    user.save()
    # continue the pipeline
    return
