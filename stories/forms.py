from django import forms
from django.forms import widgets
from django.core.validators import MinLengthValidator
from .models import Story, Chapter


class CreateStoryForm(forms.Form):
    title = forms.CharField(min_length=Story.MIN_TITLE_LEN,
                            max_length=Story.MAX_TITLE_LEN)
    # next is about first chapter:
    headline = forms.CharField(min_length=Chapter.MIN_HEADLINE_LEN,
                               max_length=Chapter.MAX_HEADLINE_LEN,
                               label='Headline of first chapter')
    body = forms.CharField(min_length=Chapter.MIN_BODY_LEN,
                           max_length=Chapter.MAX_BODY_LEN,
                           widget=widgets.Textarea(),
                           label='Body of first chapter')


class AddChapterForm(forms.ModelForm):
    class Meta:
        model = Chapter
        fields = ['parent', 'headline', 'body']
        widgets = {
            'parent': widgets.HiddenInput(),
            'body': widgets.Textarea(),
        }
    
    def __init__(self, user=None, *args, **kwargs):
        super(AddChapterForm, self).__init__(*args, **kwargs)
        self.user = user
        headline_min_len_val = MinLengthValidator(Chapter.MIN_HEADLINE_LEN)
        self.fields['headline'].validators.append(headline_min_len_val)
        body_min_len_val = MinLengthValidator(Chapter.MIN_BODY_LEN)
        self.fields['body'].validators.append(body_min_len_val)
    
    def save(self, *args, **kwargs):
        created_chapter = super(AddChapterForm, self).save(*args, **kwargs)
        if self.user and self.user.is_authenticated():
            created_chapter.author = self.user
            created_chapter.save()
        return created_chapter

