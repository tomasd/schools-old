# Create your views here.
def companies(request, **kwargs):
    if 'extra_context' not in kwargs: kwargs['extra_context'] = {}
    
    kwargs['extra_context']['action_form'], response = serve_delete_action_form(
        request, queryset, reverse('buildings'))
    if response is not None:
        return response