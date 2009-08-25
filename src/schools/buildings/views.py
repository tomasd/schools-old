# Create your views here.
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template.context import RequestContext
from schools import object_list, serve_delete_action_form
from schools.buildings.forms import ClassroomForm, BuildingMonthExpenseForm
from schools.buildings.models import Building, Classroom, BuildingMonthExpense


@login_required
def classrooms(request, building_id, **kwargs):
    building = get_object_or_404(Building, pk=building_id)
    queryset = Classroom.objects.filter(building__pk=building_id)
    if 'extra_context' not in kwargs: kwargs['extra_context'] = {}
    
    kwargs['extra_context']['building'] = building
    kwargs['extra_context']['action_form'], response = serve_delete_action_form(request, queryset)
    if response is not None:
        return response
    return object_list(request, queryset=queryset, **kwargs)

@login_required
def classroom_create(request, building_id):
    building = get_object_or_404(Building, pk=building_id)
    classroom = Classroom(building=building)
    if request.method == 'POST':
        form = ClassroomForm(request.POST, instance=classroom)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(form.instance.get_absolute_url())
    else:
        form = ClassroomForm(instance=classroom)
    return render_to_response('buildings/building_classroom_create.html',
                              {'form':form,
                               'building':building}, context_instance=RequestContext(request))
    
@login_required
def classroom_detail(request, building_id, classroom_id):
    building = get_object_or_404(Building, pk=building_id)
    classroom = get_object_or_404(building.classroom_set.all(), pk=classroom_id)
    if request.method == 'POST':
        form = ClassroomForm(request.POST, instance=classroom)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(form.instance.get_absolute_url())
    else:
        form = ClassroomForm(instance=classroom)
    return render_to_response('buildings/building_classroom_form.html',
                              {'form':form,
                               'building':building}, context_instance=RequestContext(request))

@login_required
def building_expenses(request, building_id, **kwargs):
    building = get_object_or_404(Building, pk=building_id)
    if 'extra_context' not in kwargs: kwargs['extra_context'] = {}
    
    kwargs['extra_context']['building'] = building
    queryset = BuildingMonthExpense.objects.filter(building__pk=building_id)
    return object_list(request, queryset=queryset, **kwargs)

@login_required
def building_expense_create(request, building_id, **kwargs):
    building = get_object_or_404(Building, pk=building_id)
    building_expense = BuildingMonthExpense(building=building)
    if request.method == 'POST':
        form = BuildingMonthExpenseForm(request.POST, instance=building_expense)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(form.instance.get_absolute_url())
    else:
        form = BuildingMonthExpenseForm(instance=building_expense)
    return render_to_response('buildings/building_expense_create.html',
                              {'form':form,
                               'building':building}, context_instance=RequestContext(request))
    
@login_required
def building_expense_detail(request, building_id, building_expense_id):
    building = get_object_or_404(Building, pk=building_id)
    building_expense = get_object_or_404(building.buildingmonthexpense_set.all(), pk=building_expense_id)
    if request.method == 'POST':
        form = BuildingMonthExpenseForm(request.POST, instance=building_expense)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(form.instance.get_absolute_url())
    else:
        form = BuildingMonthExpenseForm(instance=building_expense)
    return render_to_response('buildings/building_expense_form.html',
                              {'form':form,
                               'building':building}, context_instance=RequestContext(request))
    
