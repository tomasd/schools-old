from django import forms
from django.contrib.auth.views import redirect_to_login
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext as _
from django.views.generic import list_detail


def object_list(request, **kwargs):
    if 'login_required' in kwargs:
        if kwargs['login_required'] and not request.user.is_authenticated():
            return redirect_to_login(request.path)
        kwargs.pop('login_required')
        
    queryset = kwargs['queryset']
    if 'extra_context' not in kwargs: kwargs['extra_context'] = {}
    
    kwargs['extra_context']['action_form'], response = serve_delete_action_form(
        request, queryset)
    if response is not None:
        return response
    
    return list_detail.object_list(request, **kwargs)

class ActionForm(forms.Form):
    objects = forms.ModelMultipleChoiceField(queryset=None, required=False)
    action = forms.ChoiceField(label=_('Action'), required=False)
    
    def __init__(self, queryset, actions, *args, **kwargs):
        super(ActionForm, self).__init__(*args, **kwargs)
        self.fields['objects'].queryset = queryset
        self.fields['action'].choices = [('', "---------")] + actions
        
def serve_delete_action_form(request, queryset):
    '''
        Process delete action form. Returns tuple (form, response).
        When response is not None, then it should be returned from 
        the view function.
    '''
    if request.method== 'POST':
        form = ActionForm(queryset, [('delete', _('Delete'))], request.POST)
        if form.is_valid():
            if form.cleaned_data['action'] == 'delete':
                for obj in form.cleaned_data['objects']:
                    obj.delete()
            return form, HttpResponseRedirect(request.path)
    else:
        form = ActionForm(queryset, [('delete', _('Delete'))])
    return form, None