# Create your views here.
from datetime import datetime, date
from django.contrib.auth.decorators import login_required
from django.forms.models import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template.context import RequestContext
from schools.courses.forms import CourseMemberForm, CourseMemberCreateForm, \
    LessonForm, AttendanceListForm, ExpenseGroupCreateForm, ExpenseGroupForm, \
    LessonAttendeeCreateForm
from schools.courses.models import Course, CourseMember, Lesson, AttendanceList, \
    ExpenseGroup, ExpenseGroupPrice, course_member_price, course_members_on_lesson
from schools.lectors.models import lector_price
from schools.testing.models import TestResult, CourseMemberAssessment

@login_required
def course_members(request, slug):
    course = get_object_or_404(Course, slug=slug)
    
    course_member = CourseMember(course=course, start=datetime.today())
    if request.method == 'POST':
        form = CourseMemberCreateForm(course, request.POST, instance=course_member)
        if form.is_valid():
            course_member = form.save(commit=False)
            if form.cleaned_data['price'] is not None and form.cleaned_data['expense_group'] is None:
                course_member.create_individual_expense_group(form.cleaned_data['price'])
            else:
                course_member.expense_group = form.cleaned_data['expense_group']
            course_member.save()
            return HttpResponseRedirect(form.instance.get_absolute_url())
    else:
        form = CourseMemberCreateForm(course, instance=course_member)
    
    return render_to_response('courses/course_member_list.html',
          {'course':course, 'member_list': course.coursemember_set.all(),
           'create_member':form },
                  context_instance=RequestContext(request))

@login_required
def course_lessons(request, slug):
    course = get_object_or_404(Course, slug=slug)
    
    course_lesson = Lesson(course=course)
    if request.method == 'POST':
        form = LessonForm(request.POST, instance=course_lesson)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(form.instance.get_absolute_url())
    else:
        form = LessonForm(instance=course_lesson)
    
    return render_to_response('courses/course_lesson_list.html',
          {'course':course, 'lesson_list': course.lesson_set.all(),
           'create_lesson':form },
                  context_instance=RequestContext(request))

@login_required
def course_member_detail(request, slug, member_id):
    course = get_object_or_404(Course, slug=slug)
    course_member = get_object_or_404(course.coursemember_set.all(), pk=member_id)
    
    TestResultFormset = inlineformset_factory(CourseMember, TestResult, extra=1)
    CourseMemberAssessmentFormset = inlineformset_factory(CourseMember, CourseMemberAssessment, extra=1)
    
    if request.method == 'POST':
        form = CourseMemberForm(request.POST, instance=course_member)
        test_form = TestResultFormset(request.POST, instance=course_member)
        assessment_form = CourseMemberAssessmentFormset(request.POST, instance=course_member)
        if form.is_valid() and test_form.is_valid() and assessment_form.is_valid():
            form.save()
            test_form.save()
            assessment_form.save()
            return HttpResponseRedirect(form.instance.get_absolute_url())
    else:
        form = CourseMemberForm(instance=course_member)
        test_form = TestResultFormset(instance=course_member)
        assessment_form = CourseMemberAssessmentFormset(instance=course_member)
        
    return render_to_response('courses/course_member_form.html',
          {'course':course, 'form':form, 'test_form':test_form, 'assessment_form': assessment_form,
           'member_list':course.coursemember_set.all()}, context_instance=RequestContext(request))

@login_required 
def course_lesson_detail(request, slug, lesson_id):
    course = get_object_or_404(Course, slug=slug)
    course_lesson = get_object_or_404(course.lesson_set.all(), pk=lesson_id)
    
    if request.method == 'POST':
        lesson_form = LessonForm(request.POST, instance=course_lesson)
        if lesson_form.is_valid():
            lesson_form.save()
            return HttpResponseRedirect(lesson_form.instance.get_absolute_url())
    else:
        lesson_form = LessonForm(instance=course_lesson)
        
    return render_to_response('courses/course_lesson_form.html',
          {'course':course, 'form':lesson_form,
           'lesson_list':course.lesson_set.all()}, context_instance=RequestContext(request))

def _course_attendance_list_create(request, course, course_lesson, attendance_list):
    if request.method == 'POST':
        form = AttendanceListForm(request.POST, instance=attendance_list)
        start, end = (form.cleaned_data['start'], form.cleaned_data['end']) if form.is_valid() else (attendance_list.start, attendance_list.end)
        course_members = course_members_on_lesson(course, start, end)
        attendee_form = LessonAttendeeCreateForm(course_members, request.POST)
        
        if form.is_valid() and attendee_form.is_valid():
            form.instance.lector_price = lector_price(form.cleaned_data['lector'],
                      course, form.cleaned_data['start'], form.cleaned_data['end'])
            attendance_list = form.save()
            
            for course_member in course_members:
                attendee = {'present':course_member in attendee_form.cleaned_data['course_members'],
                            'course_member':course_member,
                            'course_member_price':course_member_price(course_member, start, end, course_members)}
                attendance_list.lessonattendee_set.create(**attendee)
            
            return HttpResponseRedirect(attendance_list.get_absolute_url())
    else:
        form = AttendanceListForm(instance=attendance_list)
        attendee_form = LessonAttendeeCreateForm(course_members_on_lesson(course, attendance_list.start, attendance_list.end))
    return render_to_response('courses/course_attendance_list_create.html',
                  {'form':form, 'attendee_form':attendee_form,
                   'lesson_list':course.lesson_set.all(), 'course':course},
                  context_instance=RequestContext(request))

def _course_attendance_list_detail(request, course, course_lesson, attendance_list):
    course_members = CourseMember.objects.filter(lessonattendee__attendance_list=attendance_list)
    checked_course_members = {'course_members':[a.course_member.pk for a in attendance_list.lessonattendee_set.all() if a.present]}
    if request.method == 'POST':
        form = AttendanceListForm(request.POST, instance=attendance_list)
        attendee_form = LessonAttendeeCreateForm(course_members, request.POST, initial=checked_course_members)
        if form.is_valid() and attendee_form.is_valid():
            form.instance.lector_price = lector_price(form.cleaned_data['lector'],
                      course, form.cleaned_data['start'], form.cleaned_data['end'])
            attendance_list = form.save()
            
            for lesson_attendee in attendance_list.lessonattendee_set.all():
                lesson_attendee.present = lesson_attendee.course_member in attendee_form.cleaned_data['course_members']
                lesson_attendee.course_member_price = course_member_price(lesson_attendee.course_member, attendance_list.start, attendance_list.end, course_members)
                lesson_attendee.save()
                    
    else:
        form = AttendanceListForm(instance=attendance_list)
        attendee_form = LessonAttendeeCreateForm(course_members, initial=checked_course_members)
    return render_to_response('courses/course_attendance_list_form.html',
                { 'lesson_list':course.lesson_set.all(), 'course':course,
                 'form':form, 'attendee_form':attendee_form},
                context_instance=RequestContext(request))

@login_required
def course_attendance_list(request, slug, lesson_id):
    course = get_object_or_404(Course, slug=slug)
    course_lesson = get_object_or_404(course.lesson_set.all(), pk=lesson_id)
    try:
        return _course_attendance_list_detail(request, course, course_lesson, course_lesson.attendancelist)
    except AttendanceList.DoesNotExist: #@UndefinedVariable
        return _course_attendance_list_create(request, course, course_lesson, course_lesson.create_attendance_list())

@login_required    
def course_expense_groups_list(request, slug):
    course = get_object_or_404(Course, slug=slug)
    
    expense_group = ExpenseGroup(course=course)
    if request.method == 'POST':
        form = ExpenseGroupCreateForm(request.POST, instance=expense_group)
        if form.is_valid():
            expense_group = form.save()
            expense_group.expensegroupprice_set.create(start=form.cleaned_data['start'],
                                                       end=form.cleaned_data['end'],
                                                       price=form.cleaned_data['price'])
            return HttpResponseRedirect(form.instance.get_absolute_url())
    else:
        form = ExpenseGroupCreateForm(initial={'start':date.today()})
        
    return render_to_response('courses/course_expense_groups_list.html',
                  {'course':course,
                   'create_expense_group':form,
                   'expense_group_list': course.expensegroup_set.all(), },
                  context_instance=RequestContext(request))

@login_required
def course_expense_group_detail(request, slug, expense_group_id):
    course = get_object_or_404(Course, slug=slug)
    expense_group = get_object_or_404(course.expensegroup_set.all(), pk=expense_group_id)

    PriceForm = inlineformset_factory(ExpenseGroup, ExpenseGroupPrice, extra=1, can_delete=False)
    
    if request.method == 'POST':
        form = ExpenseGroupForm(request.POST, instance=expense_group)
        price_form = PriceForm(request.POST, instance=expense_group)
        if form.is_valid() and price_form.is_valid():
            form.save()
            price_form.save()
            return HttpResponseRedirect(form.instance.get_absolute_url())
    else:
        form = ExpenseGroupForm(instance=expense_group)
        price_form = PriceForm(instance=expense_group)
        
    return render_to_response('courses/course_expense_group_form.html',
          {'course':course, 'form':form, 'price_form':price_form,
           'expense_group_list':course.expensegroup_set.all()},
           context_instance=RequestContext(request))
