from django.contrib.auth.decorators import login_required
from django.conf.urls import patterns, url
from general.decorators import ajax_only
from .views import CreateStoryView, StoryDetailView, ReadStoryView, BookmarksView, \
    ChapterDetailAjaxView, AddChapterAjaxView, ChapterFeedbackAjaxView


urlpatterns = patterns('',
    url(r'^start-story/$', login_required(CreateStoryView.as_view()), name='create_story'),
    url(r'^story/(?P<pk>\d+)/$', StoryDetailView.as_view(), name='story_detail'),
    url(r'^story/(?P<pk>\d+)/read/$', ReadStoryView.as_view(), name='read_story'),
    url(r'^bookmarks/$', login_required(BookmarksView.as_view()), name='bookmarks'),
    
    url(r'^ajax/chapter/(?P<pk>\d+)/$',
        ajax_only(ChapterDetailAjaxView.as_view()), 
        name='chapter_detail_ajax'),
    url(r'^ajax/add-chapter/$',
        ajax_only(login_required(AddChapterAjaxView.as_view())), 
        name='add_chapter_ajax'),
    url(r'^ajax/chapter-feedback/(?P<pk>\d+)/$',
        ajax_only(login_required(ChapterFeedbackAjaxView.as_view())),
        name='chapter_feedback_ajax'),
)

