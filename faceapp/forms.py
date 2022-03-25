from django import forms
from .models import Face

class NewPhotoForm(forms.ModelForm):
  class Meta:
    model = Face
    fields = ['images']
