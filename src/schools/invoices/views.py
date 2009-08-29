# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib.formtools.wizard import FormWizard
from schools import ModelSelectForm
from schools.invoices.forms import InvoiceForm
from schools.courses.models import LessonAttendee
from django.forms.widgets import CheckboxSelectMultiple
from django.utils.translation import ugettext as _

class CreateInvoiceWizard(FormWizard):
    def done(self, request, form_list):
        pass
    
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
        invoice = invoice_form.save(commit=False)
        
        return 
@login_required
def create_invoice(request):
    return CreateInvoiceWizard([InvoiceForm, ModelSelectForm])(request)
