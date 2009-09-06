from django import forms
from schools.testing.models import Test
from django.utils.translation import ugettext_lazy as _

class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        
