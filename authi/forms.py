from django import forms
from .models import todo


class formm(forms.ModelForm):
    class Meta:
        model = todo
        fields = ['task', 'dat', 'select']