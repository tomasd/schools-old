from django import forms
from schools.invoices.models import Invoice

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice