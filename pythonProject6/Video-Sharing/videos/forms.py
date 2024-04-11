# videos/forms.py

from django import forms
from .models import Video

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'description', 'video_file', 'thumbnail']

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.',
                             widget=forms.TextInput(attrs={'placeholder': 'Enter your email'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

from .models import ProductionLog

class ProductionLogForm(forms.ModelForm):
    class Meta:
        model = ProductionLog
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        # Perform any additional validation or cleaning here if needed
        return cleaned_data