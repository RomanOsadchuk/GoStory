from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.shortcuts import get_object_or_404

from django.db.models import Count
from stories.models import Chapter


class RegistrationView(FormView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = '/'
    
    def form_valid(self, form):
        name = form.cleaned_data['username']
        password = form.cleaned_data['password1']
        user = User.objects.create_user(name, None, password)
        new_user = authenticate(username=name, password=password)
        login(self.request, new_user)
        return super(RegistrationView, self).form_valid(form)


class ProfileView(TemplateView):
    CHAPTERS_NUMBER = 4
    template_name = 'registration/profile.html'
    
    def get_context_data(self, *args, **kwargs):
        context = super(ProfileView, self).get_context_data(*args, **kwargs)
        prof_user = get_object_or_404(User, username=kwargs['username'])
        chapters = Chapter.objects.filter(author=prof_user)
        chapters = chapters.annotate(likes_num=Count('likers'))
        context = {
            'profile_user': prof_user,
            'written_chapters_num': prof_user.chapter_set.all().count(),
            'read_chapters_num': prof_user.read_chapters.all().count(),
            'last_written_chapters': chapters.order_by('-added_at')[:self.CHAPTERS_NUMBER],
            'best_written_chapters': chapters.order_by('-likes_num')[:self.CHAPTERS_NUMBER],
        }
        return context

