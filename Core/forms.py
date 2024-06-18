from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import ITPersonnel

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = ITPersonnel
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = ITPersonnel
        fields = ('email',)