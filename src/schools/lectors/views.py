# Create your views here.
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template.context import RequestContext
from schools.lectors.forms import ContractForm
from schools.lectors.models import Lector, Contract, HourRate
from django.forms.models import inlineformset_factory

@login_required
def contracts(request, lector_id):
    lector = get_object_or_404(Lector, pk=lector_id)
    
    contracts = lector.contract_set.all()
    if request.method == 'POST':
        form = ContractForm(request.POST, instance=Contract(lector=lector))
        if form.is_valid():
            contract = form.save()
            return HttpResponseRedirect(contract.get_absolute_url())
    else:
        form = ContractForm()
    
    return render_to_response('lectors/lector_contract_list.html',
              {'contracts':contracts, 'lector':lector,
               'form':form},
              context_instance=RequestContext(request))

@login_required
def contract_detail(request, lector_id, contract_id):
    lector = get_object_or_404(Lector, pk=lector_id)
    contract = get_object_or_404(lector.contract_set, pk=contract_id)
    
    HourRateFormset = inlineformset_factory(Contract, HourRate)
    
    if request.method == 'POST':
        form = ContractForm(request.POST, instance=contract)
        hourrate_form = HourRateFormset(request.POST, instance=contract)
        if form.is_valid() and hourrate_form.is_valid():
            contract = form.save()
            hourrate_form.save()
            return HttpResponseRedirect(contract.get_absolute_url())
    else:
        form = ContractForm(instance=contract)
        hourrate_form = HourRateFormset(instance=contract)
        
    return render_to_response('lectors/lector_contract_form.html',
              {'form':form, 'lector':lector, 'hourrate_form':hourrate_form,
               'contracts':lector.contract_set.all()},
              context_instance=RequestContext(request))
