import pdb

from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.http import Http404

from .models import Game
from django.contrib.auth.models import User

# Create your views here.

def group_required(*groups):
    """Requires user membership in at least one of the groups passed in.
    Source: Django Snippets"""
    def in_groups(u):
        if u.is_authenticated:
            if bool(u.groups.filter(name__in=groups)) | u.is_superuser:
                return True
        return False
    return user_passes_test(in_groups)

def game_player_required(function):
    """Decorator to permit only the gameowner to update the game.
    
    The game should be passed into the function as a url parameter named 'game'.
    If the game is not found in the database, Http404 is raised. If the user does
    not own the game, PermissionDenied is raised.
    """
    def wrap(request, *args, **kwargs):
        """Wrapper returns the decorated function if permitted, else returns PermissionDenied"""
        games = request.user.gameplayed_set.all() #games played by the user
        try:
            game = Game.objects.get(pk=kwargs['game'])
        except:
            raise Http404
        if request.user.is_authenticated and game in [game_played.game for game_played in games]:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return wrap

def game_developer_required(function):
    """Decorator to permit only the game developer to update the game"""
    def wrap(request, *args, **kwargs):
        """Wrapper returns the decorated function if permitted, else returns PermissionDenied"""
        game = Game.objects.get(pk=kwargs['game'])
        if request.user.is_authenticated and game.developer.id == request.user.id:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return wrap

def profile_owner_required(function):
    """Decorator to permit only the profile owner to update the profile"""
    def wrap(request, *args, **kwargs):
        """Wrapper returns the decorated function if permitted, else returns PermissionDenied"""
        user = User.objects.get(pk=kwargs['pk'])
        if request.user.is_authenticated and user.id == request.user.id:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return wrap
