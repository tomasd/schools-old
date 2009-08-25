from django import forms
from schools.testing.models import Test, TestResult

class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        
