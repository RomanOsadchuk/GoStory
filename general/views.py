from django.views.generic.base import TemplateView
from stories.services import AuthorService, StoryService


class HomeView(TemplateView):
    template_name = 'general/home.html'
    STORY_LIMIT = 5
    AUTHOR_LIMIT = 6

    def get_context_data(self, *args, **kwarks):
        context = super(HomeView, self).get_context_data(*args, **kwarks)
        context.update({
            'recent_stories': StoryService.get_recent(self.STORY_LIMIT),
            'interesting_stories': StoryService.get_interesting(self.STORY_LIMIT),
            'best_writers': AuthorService.get_most_writable(self.AUTHOR_LIMIT)
        })
        return context

