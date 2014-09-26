from django.db.models import Count
from django.core.urlresolvers import reverse
from django.http import JsonResponse
from django.views.generic import View, DetailView, TemplateView
from django.views.generic.edit import FormView
from django.shortcuts import render, redirect, get_object_or_404

from .models import Story, Chapter
from .forms import CreateStoryForm, AddChapterForm


class BookmarksView(TemplateView):
    template_name = 'stories/bookmarks.html'
    
    def get_context_data(self, *args, **kwargs):
        context = super(BookmarksView, self).get_context_data(*args, **kwargs)
        user = self.request.user
        context['bookmarks'] = user.bookmarks.all().order_by('story')
        return context


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
    MAIN_AUTHORS_NUM = 5
    model = Story
    
    def get_context_data(self, *args, **kwargs):
        context = super(StoryDetailView, self).get_context_data(*args, **kwargs)
        chapters = Chapter.objects.filter(story=self.object)
        context['chapter_num'] = chapters.count()
        context['authors'] = chapters.values('author__username').annotate(
            chap_num=Count('id')).order_by('-chap_num')[:self.MAIN_AUTHORS_NUM]
        return context


class ChapterDetailAjaxView(TemplateView):
    template_name = 'stories/chapter_single.html'
    
    def get_chapter_pk(self):
        chapter_pk = self.kwargs.get('pk')
        return chapter_pk
    
    @classmethod
    def get_chapter_context(cls, chapter_pk):
        chapter = Chapter.objects.filter(pk=chapter_pk
            ).select_related('readers', 'bookmarkers', 'likers')[0]
        context = {
            'chapter': chapter,
            'neighbours': Chapter.objects.filter(parent=chapter.parent
                              ).exclude(pk=chapter.pk).only('headline'),
            'children': Chapter.objects.filter(parent=chapter).only('headline'),
        }
        if chapter.parent:
            initial = {'parent': chapter.parent}
            form = AddChapterForm(initial=initial)
            context['form'] = form
        return context
    
    def get_context_data(self, *args, **kwargs):
        context = super(ChapterDetailAjaxView, self).get_context_data(*args, **kwargs)
        chapter_pk = self.get_chapter_pk()
        context.update(self.get_chapter_context(chapter_pk))
        chapter = context['chapter']
        user = self.request.user
        if user.is_authenticated():
            chapter.readers.add(user)
            context['bookmarked'] = user in chapter.bookmarkers.all()
            context['liked'] = user in chapter.likers.all()
        return context


class ReadStoryView(ChapterDetailAjaxView):
    template_name = 'stories/story_read.html'
    
    def get_chapter_pk(self):
        story = get_object_or_404(Story, pk=self.kwargs['pk'])
        chapter_pk = self.request.GET.get('bookmark') or \
                     self.request.GET.get('chapter-pk')
        if chapter_pk:
            chapter = get_object_or_404(Chapter, pk=chapter_pk)
            # if chapter.story != story: 
        else:
            chapter = Chapter.objects.get(story=story, parent__isnull=True)
        return chapter.pk

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
            context = ChapterDetailAjaxView.get_chapter_context(chapter.pk)
            return render(request, 'stories/chapter_single.html', context)
        else:
            data = form.errors.as_json()
            response = JsonResponse(data=data, safe=False, status=400)
            return response


class ChapterFeedbackAjaxView(View):
    def get(self, request, *args, **kwargs):
        chapter = get_object_or_404(Chapter, pk=kwargs['pk'])
        feedback_type = request.GET.get('feedback_type')
        if feedback_type == 'add-bookmark':
            chapter.bookmarkers.add(request.user)
        elif feedback_type == 'remove-bookmark':
            chapter.bookmarkers.remove(request.user)
        elif feedback_type == 'like':
            chapter.likers.add(request.user)
        elif feedback_type == 'cancel-like':
            chapter.likers.remove(request.user)
        else:
            data = {'message': 'unknown feedback type'}
            return JsonResponse(data=data, safe=False, status=400)
        return JsonResponse(data={'message': 'OK'}, safe=False) 

