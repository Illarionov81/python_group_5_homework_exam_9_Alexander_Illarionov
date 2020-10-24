from django import forms

from webapp.models import Gallery


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Gallery
        fields = ['photo', 'signature']






