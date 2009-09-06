from django import forms
from schools.students.models import Student
from django.utils.translation import ugettext_lazy as _

class StudentForm(forms.ModelForm):
    class Meta:
        fields = ('last_name', 'first_name', 'company', 'title',
                  'street', 'postal', 'town', 
                  'phone', 'mobile', 'fax', 'www', 'email',)
        model = Student