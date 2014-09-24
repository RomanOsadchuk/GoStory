from django.core.urlresolvers import reverse
from django.http import JsonResponse
from django.views.generic import View, DetailView, TemplateView
from django.views.generic.edit import FormView
from django.shortcuts import render, redirect, get_object_or_404

from .models import Story, Chapter
from .forms import CreateStoryForm, AddChapterForm


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
        kwargs = {'pk': self.new_story.pk}
        return reverse('story_detail', kwargs=kwargs)


class StoryDetailView(DetailView):
    model = Story
    # def get_context_data(self, *args, **kwargs):
    #     context = super(StoryDetailView, self).get_context_data(*args, **kwargs)
    #     return context


class ChapterDetailAjaxView(TemplateView):
    template_name = 'stories/chapter_single.html'
    
    def get_chapter(self):
        chapter_pk = self.kwargs.get('pk') or self.request.GET['chapter-pk']
        chapter = get_object_or_404(Chapter, pk=chapter_pk)
        return chapter
    
    @classmethod
    def get_chapter_context(cls, chapter):
        context = {'chapter': chapter}
        context['neighbours'] = Chapter.objects.filter(parent=chapter.parent
            ).exclude(pk=chapter.pk).only('headline')
        context['children'] = Chapter.objects.filter(parent=chapter
            ).only('headline')
        if chapter.parent:
            initial = {'parent': chapter.parent}
            form = AddChapterForm(initial=initial)
            context['form'] = form
        return context
    
    def get_context_data(self, *args, **kwargs):
        context = super(ChapterDetailAjaxView, self).get_context_data(*args, **kwargs)
        chapter = self.get_chapter()
        context.update(self.get_chapter_context(chapter))
        return context


class ReadStoryView(ChapterDetailAjaxView):
    template_name = 'stories/story_read.html'
    
    def get_chapter(self):
        story = get_object_or_404(Story, pk=self.kwargs['pk'])
        chapter_pk = self.request.GET.get('bookmark') or \
                     self.request.GET.get('chapter-pk')
        if chapter_pk:
            chapter = get_object_or_404(Chapter, pk=chapter_pk)
            # if chapter.story != story: 
        else:
            chapter = Chapter.objects.get(story=story, parent__isnull=True)
        return chapter

    def get_context_data(self, *args, **kwargs):
        context = super(ReadStoryView, self).get_context_data(*args, **kwargs)
        form = AddChapterForm(initial={'parent': context['chapter']})
        context['continuation_form'] = form
        return context


class AddChapterAjaxView(View):
    def post(self, request, *args, **kwargs):
        form = AddChapterForm(data=request.POST, user=request.user)
        if form.is_valid():
            chapter = form.save()
            context = ChapterDetailAjaxView.get_chapter_context(chapter)
            return render(request, 'stories/chapter_single.html', context)
        else:
            data = form.errors.as_json()
            response = JsonResponse(data=data, safe=False, status=400)
            return response

