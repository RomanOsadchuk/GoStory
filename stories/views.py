from django.core.urlresolvers import reverse
from django.http import JsonResponse
from django.views.generic import View, DetailView, TemplateView
from django.views.generic.edit import FormView
from django.shortcuts import render, redirect, get_object_or_404

from .models import Story, Chapter
from .forms import CreateStoryForm, AddChapterForm
from .services import StoryService, ChapterService


class BookmarksView(TemplateView):
    template_name = 'stories/bookmarks.html'
    
    def get_context_data(self, *args, **kwargs):
        ctx = super(BookmarksView, self).get_context_data(*args, **kwargs)
        ctx['bookmarks'] = self.request.user.bookmarks.all().order_by('story')
        return ctx


# ==== CHAPTER VIEWS ==== #

class ChapterDetailAjaxView(TemplateView):
    template_name = 'stories/chapter_single.html'
    
    def get_chapter_pk(self):
        return self.kwargs.get('pk')
    
    @classmethod
    def get_chapter_context(cls, chapter_pk):
        chapter = Chapter.objects.filter(pk=chapter_pk
            ).select_related('readers', 'bookmarkers', 'likers')[0]
        # TODO: 404
        context = {
            'chapter': chapter,
            'neighbours': chapter.neighbours.only('headline'),
            'children': chapter.children.all().only('headline'),
        }
        if chapter.parent:
            context['form'] = AddChapterForm(initial={'parent': chapter.parent})
        return context
    
    def get_context_data(self, *args, **kwargs):
        context = super(ChapterDetailAjaxView, self).get_context_data(*args, **kwargs)
        chapter_pk = self.get_chapter_pk()
        context.update(self.get_chapter_context(chapter_pk))
        chapter, user = context['chapter'], self.request.user
        if user.is_authenticated():
            chapter.readers.add(user)
            context['bookmarked'] = user in chapter.bookmarkers.all()
            context['liked'] = user in chapter.likers.all()
        return context


class AddChapterAjaxView(View):
    def post(self, request, *args, **kwargs):
        form = AddChapterForm(data=request.POST, user=request.user)
        if form.is_valid():
            chapter = form.save()
            context = ChapterDetailAjaxView.get_chapter_context(chapter.pk)
            return render(request, 'stories/chapter_single.html', context)
        else:
            data = form.errors.as_json()
            response = JsonResponse(data=data, safe=False, status=400)
            return response


class ChapterFeedbackAjaxView(View):
    def get(self, request, *args, **kwargs):
        c = get_object_or_404(Chapter, pk=kwargs['pk'])
        fbt = request.GET.get('feedback_type')
        added, responce_data = ChapterService.add_feedback(c, fbt, request.user)
        status = 200 if added else 400 
        return JsonResponse(data=responce_data, safe=False, status=status)



# ==== STORY VIEWS ==== #

class CreateStoryView(FormView):
    template_name = 'stories/story_create.html'
    form_class = CreateStoryForm
    new_story = None
    
    def form_valid(self, form):
        data = form.cleaned_data
        self.new_story = Story(title=data['title'])
        self.new_story.save()
        chapter = Chapter(story=self.new_story, author=self.request.user,
                          headline=data['headline'], body=data['body'])
        chapter.save()
        return super(CreateStoryView, self).form_valid(form)
    
    def get_success_url(self):
        return reverse('story_detail', kwargs={'pk': self.new_story.pk})


class StoryListView(TemplateView):
    template_name = 'stories/story_list.html'
    
    def get_context_data(self, *args, **kwargs):
        context = super(StoryListView, self).get_context_data(*args, **kwargs)
        params = self.request.GET.dict()
        context['stories'] = StoryService.get_story_list(**params)
        return context


class StoryDetailView(DetailView):
    model = Story
    
    def get_context_data(self, *args, **kwargs):
        context = super(StoryDetailView, self).get_context_data(*args, **kwargs)
        context.update(StoryService.get_detail_context(self.object))
        context['chapters_json'] = StoryService.get_tree_json(self.object,
                                                              self.request.user)
        return context


class ReadStoryView(ChapterDetailAjaxView):
    template_name = 'stories/story_read.html'
    
    def get_chapter_pk(self):
        story = get_object_or_404(Story, pk=self.kwargs['pk'])
        chapter_pk = self.request.GET.get('bookmark') or \
                     self.request.GET.get('chapter-pk')
        if chapter_pk:
            chapter = get_object_or_404(Chapter, pk=chapter_pk)
            # TODO: if chapter.story != story: 
        else:
            chapter = Chapter.objects.get(story=story, parent__isnull=True)
        return chapter.pk

    def get_context_data(self, *args, **kwargs):
        context = super(ReadStoryView, self).get_context_data(*args, **kwargs)
        # form = AddChapterForm(initial={'parent': context['chapter']})
        context['continuation_form'] = AddChapterForm()
        return context

