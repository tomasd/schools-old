from django import forms
from schools.companies.models import Company

class CompanyForm(forms.ModelForm):
    class Meta:
        fields = ('name', 'ico', 'dic', 'ic_dph',
                  'street', 'postal', 'town',
                  'phone', 'mobile', 'fax', 'www', 'email', )
        model = Company