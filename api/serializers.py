from django.contrib.auth.models import User

from game.models import Game, GamePlayed, PaymentDetail
from accounts.models import Profile

from rest_framework import serializers

class ProfileSerializer(serializers.ModelSerializer):
    """Serializes profiles
    """
    class Meta:
        model = Profile
        fields = ('nickname', 'description', 'image')
        ordering_fields = ('nickname', 'description')

class UserSerializer(serializers.ModelSerializer):
    """Serializes users.
    
    This serializer includes a profile field for the user, serialized with
    ProfileSerializer-
    """
    class Meta:
        model = User
        fields = ('username', 'profile')
        ordering_fields = ('username',)
    
    profile = ProfileSerializer(many=False, read_only=True)

class GameSerializer(serializers.ModelSerializer):
    """Serializes game instances. Used by the games view of the rest api.
    
    Includes pretty much all information about a game, including statistics.
    """
    
    class Meta:
        model = Game
        fields = (
            'title',
            'developer',
            'url',
            'price',
            'description',
            'gameimage',
            'gamethumb',
            'viewcount',
            'sellcount',
            'upload_date',
            'popularity',
            'average_rating',
            'revenue',
        )
        ordering_fields=(
            'title',
            'price',
            'description',
            'viewcount',
            'sellcount',
            'upload_date',
            'popularity',
            'revenue'
        )
    
    developer = serializers.SlugRelatedField(
        slug_field='username',
        many=False,
        read_only=True
    )
    average_rating = serializers.FloatField(source='get_rating', read_only=True)

class GamePlayedSerializer(serializers.ModelSerializer):
    """Serializes GamePlayed instances for the user-games view. Includes the title of
    the game.
    """
    class Meta:
        model = GamePlayed
        fields = ('game', 'gameScore', 'rating')
        ordering_fields = ('gameScore', 'rating')
    
    game = serializers.SlugRelatedField(
        slug_field='title',
        many=False,
        read_only=True
    )

class UserGamePlayedSerializer(serializers.ModelSerializer):
    """Serializes GamePlayed instances for the game-buyers view. Includes the username
    of the buyer.
    """
    class Meta:
        model = GamePlayed
        fields = ('user', 'gameScore', 'rating')
        ordering_fields = ('gameScore', 'rating')
    
    user = serializers.SlugRelatedField(
        slug_field='username',
        many=False,
        read_only=True
    )
