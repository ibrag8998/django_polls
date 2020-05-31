from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView

from .forms import SignUpForm, SignInForm


def signup(req):
    form = SignUpForm(req.POST or None)
    next = reverse_lazy('users:signin')
    to_render = render(req, 'users/signup.html', {'form': form, 'next': next})

    if req.method == 'POST':
        if not form.is_valid():
            return to_render

        form.save()

        return redirect(req.POST.get('next', next))

    return to_render


class SignInView(LoginView):
    template_name = 'users/signin.html'
    authentication_form = SignInForm


class LogOutView(LogoutView):
    next_page = reverse_lazy('users:signin')
