from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class Story(models.Model):
    MIN_TITLE_LEN = 5
    MAX_TITLE_LEN = 100
    title = models.CharField(max_length=MAX_TITLE_LEN)
    slug = models.SlugField(blank=True, null=True)
    started_at = models.DateField(auto_now_add=True)
    # and it never ends =)
    # likes, genre ...
    
    def save(self, *args, **kwargs):
        # TODO: cyrilic slugs
        self.slug = slugify(self.title) or '----'
        return super(Story, self).save(*args, **kwargs)
    
    def __unicode__(self):
        return self.title


class Chapter(models.Model):
    MIN_HEADLINE_LEN = 15
    MAX_HEADLINE_LEN = 150
    MIN_BODY_LEN = 150
    MAX_BODY_LEN = 1500
    story = models.ForeignKey(Story)
    parent = models.ForeignKey('self', blank=True, null=True,
                               on_delete=models.SET_NULL, related_name='children')
    
    headline = models.CharField(max_length=MAX_HEADLINE_LEN)
    slug = models.SlugField()
    body = models.CharField(max_length=MAX_BODY_LEN)
    author = models.ForeignKey(User, blank=True, null=True,
                               on_delete=models.SET_NULL)
    added_at = models.DateTimeField(auto_now_add=True)
    
    readers = models.ManyToManyField(User, related_name='read_chapters')
    likers = models.ManyToManyField(User, related_name='liked_chapters')
    dislikers = models.ManyToManyField(User, related_name='disliked_chapters')
    bookmarkers = models.ManyToManyField(User, related_name='bookmarks')
    # auto_now_add, likes, dislikes ...
    
    def save(self, *args, **kwargs):
        # TODO: cyrilic slugs
        self.slug = slugify(self.headline) or '----'
        if not (hasattr(self, 'story') and self.story) and \
                hasattr(self, 'parent') and self.parent:
            self.story = self.parent.story
        return super(Chapter, self).save(*args, **kwargs)
    
    @property
    def neighbours(self):
        return Chapter.objects.filter(parent=self.parent).exclude(pk=self.pk)

    def __unicode__(self):
        return self.headline

