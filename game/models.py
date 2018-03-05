import logging
import re
import pdb

from decimal import Decimal

from django.conf import settings
from django.core.files import File
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q, F, Sum
from django.db.models.fields.files import ImageFieldFile, FileField
from django.utils import timezone
from PIL import Image, ImageOps
import os.path
from io import BytesIO
from django.core.files.base import ContentFile

from gameHub.settings import ImageSizeEnum

logger = logging.getLogger(__name__)

# Create your models here.

#https://stackoverflow.com/questions/34239877/django-save-user-uploads-in-seperate-folders
def user_directory_path(instance, filename):
    return 'user_{0}/game/{1}'.format(instance.developer.id, filename)

def user_directory_path_thumb(instance, filename):
    return 'user_{0}/game/thumb/{1}'.format(instance.developer.id, filename)


class Game(models.Model):
    """Game model

    referr to README.md for database schema.

    :members: title, url, description, gameimage

    .. todo::
        Relations with user models.
    """

    title         = models.TextField(max_length=300, unique=True)
    developer     = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    url           = models.URLField()
    price         = models.DecimalField(decimal_places=2, max_digits=10, validators=[MinValueValidator(Decimal('0.01'))])
    description   = models.TextField()
    gameimage     = models.ImageField(null=True, blank=True, upload_to=user_directory_path)
    gamethumb     = models.ImageField(null=True, blank=True, upload_to=user_directory_path_thumb)
    viewcount     = models.PositiveIntegerField(default=0)
    sellcount     = models.PositiveIntegerField(default=0)
    upload_date   = models.DateTimeField(default=timezone.now)
    ratings       = models.PositiveIntegerField(default=0)
    total_rating  = models.PositiveIntegerField(default=0)
    popularity    = models.FloatField(default=0.0)
    revenue       = models.DecimalField(decimal_places=2, max_digits=10, default=Decimal('0.00'))

    class Meta:
        ordering = ['viewcount', 'sellcount']

    def calculate_popularity(self):
        """Calculates the popularity of a game. The popularity is used by the search
        function to order the query results.

        .. note:: This function should be called by the methods which alter the popularity. Do not call it directly.
        """
        if self.ratings is 0:
            self.popularity = self.sellcount * 1.0
        else:
            self.popularity = self.sellcount * (self.total_rating / self.ratings)

    def increment_viewcount(self):
        """Increments the viewcount. This method should be used instead of directly
        modifying model instances to avoid race conditions, and ensure that all the
        required modifications are made to the instance.
        """
        self.viewcount = F('viewcount') + 1
        self.save()

    def increment_sellcount(self, **kwargs):
        """Increments the sellcount. This method should be used instead of directly
        modifying model instances to avoid race conditions, and ensure that all the
        required modifications are made to the instance.
        
        This method is automatically called by a signal handler when a PaymentDetail
        object is saved.
        
        Args:
            price - The price the game was bought for (optional)
        """
        self.sellcount = F('sellcount') + 1
        self.calculate_popularity()
        if 'price' in kwargs:
            self.revenue = F('revenue') + kwargs['price']
        self.save()


    def add_rating(self, rating):
        """
        .. note:: Use GamePlayed.set_rating rather than calling this function directly.
        """
        self.ratings = F('ratings') + 1
        self.total_rating = F('total_rating') + rating
        self.save()
        #double save here is neccessary since calculate_popularity requires float
        #arithmetic. F expressions forces it to SQL which does integer arithmetic
        self.refresh_from_db()
        self.calculate_popularity()
        self.save()

    def remove_rating(self, rating):
        """
        .. note:: Use GamePlayed.set_rating rather than calling this function directly.
        """
        self.ratings = F('ratings') - 1
        self.total_rating = F('total_rating') + rating
        self.save()
        #double save here is neccessary since calculate_popularity requires float
        #arithmetic. F expressions forces it to SQL which does integer arithmetic
        self.refresh_from_db()
        self.calculate_popularity()
        self.save()

    def change_rating(self, change):
        """
        .. note:: Use GamePlayed.set_rating rather than calling this function directly.
        """
        self.total_rating = F('total_rating') + change
        self.save()
        #double save here is neccessary since calculate_popularity requires float
        #arithmetic. F expressions forces it to SQL which does integer arithmetic
        self.refresh_from_db()
        self.calculate_popularity()
        self.save()
    
    def get_rating(self):
        """Returns the calculated rating. Simply total_rating / ratings, or 0 if no
        ratings have been given.
        """
        if self.ratings > 0:
            return self.total_rating / self.ratings
        else:
            return 0
    
    def get_rating_cleaned(self):
        """Returns the ratings as they should be read by the game/rating.html
        template.

        The game/rating template requires the rating to be given times a factor of
        two to permit half stars to be given as an integer. Examples, 10 is 5 stars,
        5 is 2 and a half star.
        """
        if self.ratings > 0:
            return int((self.total_rating / self.ratings) * 2 + 0.5)
        else:
            return 0
    
    @staticmethod
    def resize_image(image, name, size):
        if not isinstance(size, ImageSizeEnum):
            raise ValueError
        image_name, image_extension = os.path.splitext(name)
        # PIL Python Image Library
        image_pil = Image.open(image)
        # Check correct image extension, ex. user renamed .png to .jpg
        if image_extension in ['.jpg', '.jpeg'] and image_pil.mode in ('RGBA', 'LA'):
            image_extension = '.png'
        image_name = image_name + image_extension # Save img with correct extension
        image_resize = ImageOps.fit(image_pil, size.value, Image.ANTIALIAS)  # Resize image
        if image_extension in ['.jpg', '.jpeg']:
            FTYPE = 'JPEG'
        elif image_extension == '.gif':
            FTYPE = 'GIF'
        elif image_extension == '.png':
            FTYPE = 'PNG'
        else:
            # ToDo Find correct exception
            raise ValueError
        image_stream = BytesIO()
        image_resize.save(image_stream, FTYPE)
        image_stream.seek(0)
        resize_image = InMemoryUploadedFile(image_stream, None, image_name, FTYPE, image_stream.tell(), None)
        return resize_image

    @classmethod
    def create(cls, title, url, developer, price = 0.0, description='', gameimage=None, gamethumb=None,viewcount=0):
        """Creates an object. Use this function instead of calling the class
        constructor.
        """

        game = cls(
            title=title,
            url=url,
            price=price,
            developer = developer,
            description=description,
            gameimage=gameimage,
            gamethumb=gamethumb,
            viewcount=viewcount
        )
        return game

    @classmethod
    def search(cls, q):
        """Searches for games in the database.

        Args:
            q (str):
                The search query string. If None then it fetches all games from database

        Return:
            A queryset containing all the found games.
        """

        if q is None:
            return cls.objects.all().order_by('-popularity')
        else:
            qwords = map(lambda m: m[0] if len(m[0]) > 0 else m[1],
                re.findall(r'"(.+)"|(\S+)', q))
            query = Q()
            for word in qwords:
                query = query & (
                    Q(title__contains=word) |
                    Q(description__contains=word))

            return cls.objects.all().filter(query).order_by('-popularity')

    def __str__(self):
        return 'Game {0}, title: {1}, url: {2}'.format(
            self.pk,
            self.title,
            self.url
        )


class GamePlayed(models.Model):
    """GamePlayed model - when a user buys a game, the game is added to the
    GamePlayed database with gameState field empty, but users field with the
    user who bought the game.
    After the subsequent games, only the gameState for the user is updated.

    For storing extra information -how much a user paid for game (if needed),
    a middle model could be used in many to many relationship
    as referred to README.md for database schema.

    :members: game, gameScore, gameState, users, rating

    """

    game      = models.ForeignKey(Game, null=True, on_delete=models.SET_NULL)
    gameScore = models.IntegerField()
    gameState = models.TextField(default="{''}")
    user     = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    rating    = models.IntegerField(default=0)

    class Meta:
        unique_together = ("game", "user")

    def set_rating(self, rating):
        """Gives a rating from a user to a game.
        """
        if self.rating == 0:
            self.game.add_rating(rating)
        else:
            self.game.change_rating(rating - self.rating)
        self.rating = rating
        self.save()

    def __str__(self):
        if (self.game):
            gametitle = self.game.title
        else:
            gametitle = 'Game Deleted'
        return 'Game {0}, GameState: {1}'.format(
            gametitle,
            self.gameState
        )

class PaymentDetail(models.Model):
    """PaymentDetail model - this model is used as a link between gameplayed and
    users many to many relationship. When game is purchased, it is added here.

    :members: game_played, cost, user, selldate
    -Game purchased is stored in game_played as GamePlayed
    -cost is the price of the game
    -user is the buyer of the game
    -selldate is the date of purchase

    """
    game_played = models.OneToOneField(GamePlayed, null=True, on_delete=models.SET_NULL)
    cost = models.DecimalField(decimal_places=2, max_digits=10, validators=[MinValueValidator(Decimal('0.01'))])
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    selldate = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        if (self.user):
            user = self.user.username
        else:
            user = 'Account Deleted'
        if (self.game_played.game):
            game = self.game_played.game.title
        else:
            game = 'Game Deleted'
        return '{0} owns {1}'.format(
            user,
            game
        )
