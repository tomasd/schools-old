# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib.formtools.wizard import FormWizard
from django.core.urlresolvers import reverse
from django.forms.widgets import CheckboxSelectMultiple
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from django.utils.translation import ugettext as _
from schools import ModelSelectForm
from schools.courses.models import LessonAttendee
from schools.invoices.forms import InvoiceForm, GenerateInvoiceForm
from schools.invoices.models import Invoice, create_invoices

class CreateInvoiceWizard(FormWizard):
    def get_template(self, step):
        return 'invoices/invoice_create_%d.html' % step
    
    def get_form(self, step, data=None):
        form = self.form_list[step]
        if form == ModelSelectForm:
            queryset = LessonAttendee.objects.for_invoice(**self.extra_context)
            initial = self.initial.get(step, {})
            initial['objects'] = [a.pk for a in queryset]
            print initial
            # create ModelSelectForm
            return form(queryset=queryset, data=data,
                        prefix=self.prefix_for_step(step),
                        initial=initial,
                        widget=CheckboxSelectMultiple,
                        label=_('Lessons'))
        return super(CreateInvoiceWizard, self).get_form(step, data)

    def process_step(self, request, form, step):
        if not hasattr(form, 'cleaned_data'): 
            if not form.is_valid(): raise Exception('Not valid form')
        if isinstance(form, InvoiceForm):
            self.extra_context['company'] = form.cleaned_data['company']
            self.extra_context['start'] = form.cleaned_data['start']
            self.extra_context['end'] = form.cleaned_data['end']
            
    def done(self, request, form_list):
        [invoice_form] = [a for a in form_list if isinstance(a, InvoiceForm)]
        [attendees_form] = [a for a in form_list if isinstance(a, ModelSelectForm)]
        invoice = invoice_form.save()
        
        invoice.lessonattendee_set = attendees_form.cleaned_data['objects']
        
        return HttpResponseRedirect(invoice.get_absolute_url())
    
@login_required
def create_invoice(request):
    return CreateInvoiceWizard([InvoiceForm, ModelSelectForm])(request)

@login_required
def generate_invoice(request):
    if request.method == 'POST':
        form = GenerateInvoiceForm(request.POST)
        if form.is_valid():
            create_invoices(start=form.cleaned_data['start'], end=form.cleaned_data['end'])
            return HttpResponseRedirect(reverse('invoices'))
    else:
        form = GenerateInvoiceForm()
    return render_to_response('invoices/generate_invoices.html', 
                              {'form':form}, 
                              context_instance=RequestContext(request))

@login_required
def invoice_lesson_attendees(request, object_id):
    invoice = get_object_or_404(Invoice, pk=object_id)
    queryset = invoice.lessonattendee_set.all()
    if request.method == 'POST':
        form = ModelSelectForm(data=request.POST, queryset=queryset, initial={'objects':[a.pk for a in queryset]}, widget=CheckboxSelectMultiple, label=_('Lessons'))
        if form.is_valid():
            invoice.lessonattendee_set = form.cleaned_data['objects']
    else:
        form = ModelSelectForm(queryset=queryset, initial={'objects':[a.pk for a in queryset]}, widget=CheckboxSelectMultiple, label=_('Lessons'))
    return render_to_response('invoices/invoice_lesson_attendees.html',
                  {'form':form, 'invoice':invoice}, context_instance=RequestContext(request))

@login_required
def invoice_overview(request):
    
    return render_to_response('invoices/invoice_overview.html', {}, context_instance=RequestContext(request))