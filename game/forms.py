from django.forms import ModelForm, TextInput
from .models import Game

class UploadGameForm(ModelForm):
    """Form for uploading game.
    
    Just a straight up ModelForm.
    """

    class Meta:
        model = Game
        fields = ('title', 'url', 'price', 'description', 'gameimage')
        widgets = {
            'title': TextInput,
        }
