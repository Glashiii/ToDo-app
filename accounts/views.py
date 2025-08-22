
from django.views.generic import FormView
from django.contrib.auth import login
from .forms import SignUpForm
from django.urls import reverse_lazy



class SignUpView(FormView):
    template_name = 'signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('tasks_list')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)
