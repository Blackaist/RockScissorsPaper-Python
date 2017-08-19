from django.db import models

# Create your models here.
from django.forms import forms


class CustomImageWidget(forms.ClearableFileInput):
    input_type = 'image'

class PicsUploadForm(forms.ModelForm):
    image = forms.ImageField(widget=CustomImageWidget())
    image.widget.attrs["value"] ='Upload'