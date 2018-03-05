from django import template

register = template.Library()

@register.filter(name='owns_game')
def range_from(user, game):
    """Tells if a user owns a game
    """
    return user.gameplayed_set.filter(game=game).exists()
    