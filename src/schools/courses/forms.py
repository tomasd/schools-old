from django import forms
from schools.courses.models import Course, CourseMember, Lesson, AttendanceList, \
    ExpenseGroup, LessonAttendee
from django.utils.translation import ugettext_lazy as _
from django.forms.util import ValidationError
from django.forms.widgets import CheckboxSelectMultiple
from django.contrib.admin.widgets import AdminDateWidget, AdminSplitDateTime

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        
class CourseMemberCreateForm(forms.ModelForm):
    price = forms.DecimalField(label=_('Price'), required=False,
               help_text=_('When filled, expense group is created for this course member.'))
    expense_group = forms.ModelChoiceField(queryset=ExpenseGroup.objects.none(), label=_('Expense group'), required=False)
    start = forms.DateField(label=_('Start'), widget=AdminDateWidget)
    
    def __init__(self, course, *args, **kwargs):
        super(CourseMemberCreateForm, self).__init__(*args, **kwargs)
        self.fields['expense_group'].queryset = course.expensegroup_set.all()
    
    class Meta:
        fields = ('student', 'start',)
        model = CourseMember
        
    def clean(self):
        if self.cleaned_data['price'] is None and self.cleaned_data['expense_group'] is None:
            raise ValidationError(_('Price or expense group must be specified!'))
        return self.cleaned_data
        
class CourseMemberForm(forms.ModelForm):
    start = forms.DateField(label=_('Start'), widget=AdminDateWidget)
    end = forms.DateField(label=_('End'), widget=AdminDateWidget)
    class Meta:
        fields = ('student', 'start', 'end', 'expense_group')
        model = CourseMember

class LessonForm(forms.ModelForm):
    start = forms.DateTimeField(label=_('Start'), widget=AdminSplitDateTime)
    end = forms.DateTimeField(label=_('End'), widget=AdminSplitDateTime)
    class Meta:
        fields = ('classroom', 'start', 'end')
        model = Lesson
        
class AttendanceListForm(forms.ModelForm):
    start = forms.DateTimeField(label=_('Start'), widget=AdminSplitDateTime)
    end = forms.DateTimeField(label=_('End'), widget=AdminSplitDateTime)
    class Meta:
        fields = ('classroom', 'lector', 'start', 'end', 'content',)
        model = AttendanceList
        
class ExpenseGroupCreateForm(forms.ModelForm):
    start = forms.DateField(label=_('Start'), widget=AdminDateWidget)
    end = forms.DateField(label=_('End'), required=False, widget=AdminDateWidget)
    price = forms.DecimalField(label=_('Price'))
    class Meta:
        fields = ('name',)
        model = ExpenseGroup
        
class ExpenseGroupForm(forms.ModelForm):
    class Meta:
        fields = ('name',)
        model = ExpenseGroup
        
class LessonAttendeeForm(forms.ModelForm):
    
    
    class Meta:
        fields = ('present', )
        model = LessonAttendee

class LessonAttendeeCreateForm(forms.Form):
    course_members = forms.ModelMultipleChoiceField(CourseMember.objects.none(), widget=CheckboxSelectMultiple, required=False)

    def __init__(self, course_members, *args, **kwargs):
        super(LessonAttendeeCreateForm, self).__init__(*args, **kwargs)
        self.fields['course_members'].queryset = course_members