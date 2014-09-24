from django.contrib.auth.decorators import login_required
from django.conf.urls import patterns, url
from .views import CreateStoryView, StoryDetailView, ReadStoryView, \
    ChapterDetailAjaxView, AddChapterAjaxView


urlpatterns = patterns('',
    url(r'^start-story/$', login_required(CreateStoryView.as_view()), name='create_story'),
    url(r'^story/(?P<pk>\d+)/$', StoryDetailView.as_view(), name='story_detail'),
    url(r'^story/(?P<pk>\d+)/read/$', ReadStoryView.as_view(), name='read_story'),
    
    url(r'^ajax/chapter/(?P<pk>\d+)/$', ChapterDetailAjaxView.as_view(), name='chapter_detail_ajax'),
    url(r'^ajax/add-chapter/$', login_required(AddChapterAjaxView.as_view()), name='add_chapter_ajax'),
)

