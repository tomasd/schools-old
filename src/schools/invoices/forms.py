from django import forms
from schools.invoices.models import Invoice
from django.forms.util import ValidationError
from django.utils.translation import ugettext_lazy as _

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        
class GenerateInvoiceForm(forms.Form):
    start = forms.DateField()
    end = forms.DateField()
    
    def clean(self):
        if not self.errors:
            start = self.cleaned_data['start']
            end = self.cleaned_data['end']
            if start > end:
                raise ValidationError(_(u'Start value should be less than end value.'))
        return self.cleaned_data