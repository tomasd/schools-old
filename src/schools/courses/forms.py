from django import forms
from schools.courses.models import Course, CourseMember, Lesson, AttendanceList, \
    ExpenseGroup, LessonAttendee
from django.utils.translation import ugettext as _
from django.forms.util import ValidationError
from django.forms.widgets import HiddenInput, CheckboxSelectMultiple

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        
class CourseMemberCreateForm(forms.ModelForm):
    price = forms.DecimalField(label=_('Price'), required=False,
               help_text=_('When filled, expense group is created for this course member.'))
    expense_group = forms.ModelChoiceField(queryset=ExpenseGroup.objects.none(), label=_('Expense group'), required=False)
    
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
    class Meta:
        fields = ('student', 'start', 'end', 'expense_group')
        model = CourseMember

class LessonForm(forms.ModelForm):
    class Meta:
        fields = ('classroom', 'start', 'end')
        model = Lesson
        
class AttendanceListForm(forms.ModelForm):
    class Meta:
        fields = ('classroom', 'lector', 'start', 'end', 'content',)
        model = AttendanceList
        
class ExpenseGroupCreateForm(forms.ModelForm):
    start = forms.DateField(label=_('Start'))
    end = forms.DateField(label=_('End'), required=False)
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