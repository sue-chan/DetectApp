from django import forms                                                           
from .models import Photo

class PhotoForm(forms.Form):
    image = forms.ImageField()