from django.views.generic.base import TemplateView
from stories.models import Story


class HomeView(TemplateView):
    template_name = 'general/home.html'

    def get_context_data(self, *args, **kwarks):
        context = super(HomeView, self).get_context_data(*args, **kwarks)
        context['stories'] = Story.objects.all()
        return context
