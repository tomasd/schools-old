from django import forms
from schools.lectors.models import Contract, Lector

class ContractForm(forms.ModelForm):
    class Meta:
        model = Contract
        exclude = ('lector', )
        
class LectorForm(forms.ModelForm):
    class Meta:
        model=Lector