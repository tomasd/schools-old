from django import forms
from schools.companies.models import Company
from django.utils.translation import ugettext_lazy as _

class CompanyForm(forms.ModelForm):
    class Meta:
        fields = ('name', 'ico', 'dic', 'ic_dph',
                  'street', 'postal', 'town',
                  'phone', 'mobile', 'fax', 'www', 'email', )
        model = Company