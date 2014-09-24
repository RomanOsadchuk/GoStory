from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import FormView


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

