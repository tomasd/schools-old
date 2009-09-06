from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from schools.buildings.models import Building, Classroom, BuildingMonthExpense
from django.utils.translation import ugettext_lazy as _

class BuildingForm(forms.ModelForm):
    class Meta:
        model = Building
        
        
class ClassroomForm(forms.ModelForm):
    class Meta:
        fields = ('name', 'infinite_room',)
        model = Classroom
        
        
class BuildingMonthExpenseForm(forms.ModelForm):
    start = forms.DateField(widget=AdminDateWidget)
    end = forms.DateField(widget=AdminDateWidget)
    class Meta:
        fields = ('start', 'end', 'price')
        model = BuildingMonthExpense
