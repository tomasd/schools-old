from django import forms
from schools.lectors.models import Contract, Lector
from django.contrib.admin.widgets import AdminDateWidget
from django.utils.translation import ugettext_lazy as _

class ContractForm(forms.ModelForm):
    start = forms.DateField(label=_('Start'), widget=AdminDateWidget)
    end = forms.DateField(label=_('End'), widget=AdminDateWidget)
    class Meta:
        model = Contract
        exclude = ('lector', )
        
class LectorForm(forms.ModelForm):
    class Meta:
        model=Lector