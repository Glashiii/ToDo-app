
from allauth.account.models import EmailAddress
from allauth.account.views import LoginView
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django import forms
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView


from .forms import SignUpForm


class SignUpView(FormView):
    template_name = 'signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('account_email_verification_sent')
    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if EmailAddress.objects.filter(email__iexact=email).exists() or User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('This e-mail is already registered.')

        return email

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        if user.email:
            email_address, _ = EmailAddress.objects.update_or_create(
                user=user,
                email=user.email,
                defaults={'primary': True, 'verified': False},
            )

            email_address.send_confirmation(self.request, signup=True)


        return redirect(self.get_success_url())

class SimpleLoginView(LoginView):
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['login'].label = 'Username / email'
        form.fields['login'].widget.attrs.setdefault('placeholder', 'Username или e‑mail')
        return form


from .forms import UsernameUpdateForm


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        username_form = UsernameUpdateForm(instance=request.user)
        password_form = PasswordChangeForm(user=request.user)
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
