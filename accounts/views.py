from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import FormView
from django.contrib.auth import login, update_session_auth_hash
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


from .forms import UsernameUpdateForm


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        username_form = UsernameUpdateForm(instance=request.user)
        password_form = PasswordChangeForm(user=request.user)
        # Можно открыть вкладку из ?tab=username|password при желании
        active_form = request.GET.get('tab')
        return render(request, '../templates/tasks/profile.html', {
            'username_form': username_form,
            'password_form': password_form,
            'active_form': active_form,
        })

    def post(self, request):
        action = request.POST.get('action')
        active_form = None

        if action == 'update_profile':
            username_form = UsernameUpdateForm(request.POST, instance=request.user)
            password_form = PasswordChangeForm(user=request.user)
            if username_form.is_valid():
                username_form.save()
                messages.success(request, 'Username changed successfully.')
                return redirect('profile')
            else:
                messages.error(request, 'Check profile form.')
                active_form = 'username'

        elif action == 'change_password':
            username_form = UsernameUpdateForm(instance=request.user)
            password_form = PasswordChangeForm(user=request.user, data=request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Password changed successfully.')
                return redirect('profile')
            else:
                messages.error(request, 'Check profile form.')
                active_form = 'password'

        else:

            username_form = UsernameUpdateForm(instance=request.user)
            password_form = PasswordChangeForm(user=request.user)

        return render(request, '../templates/tasks/profile.html', {
            'username_form': username_form,
            'password_form': password_form,
            'active_form': active_form,
        })
