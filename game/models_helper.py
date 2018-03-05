from .models import GamePlayed, PaymentDetail

def buy_game_for_user(user, game):
    """Buys a game for a user. Takes as argument a User and a Game instance.
    """
    buy_game = GamePlayed.objects.create(gameScore=0)
    buy_game.game = game
    buy_game.user = user
    buy_game.save()
    PaymentDetail.objects.create(game_played=buy_game, cost=buy_game.game.price, user=user)

def rate_game_for_user(user, game, rating):
    """Rates a game for a user.

    Args:
        user - The user model instance
        game - The game model instance
        rating - the rating, as an integer in the interval [1,5]
    """
    gameplayed = user.gameplayed_set.filter(game=game)[0]
    gameplayed.set_rating(rating)
