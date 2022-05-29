from django import forms
from .models import Make


class MakeForm(forms.ModelForm):
    class Meta:
        model = Make
        fields = '__all__'
