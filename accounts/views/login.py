from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic import FormView

from accounts.forms import UserLoginForm


class AuthFormView(FormView):
    form_class = UserLoginForm
    template_name = 'booksaw/auth/login.html'

    def get_success_url(self):
        if self.request.user.is_active:
            return reverse_lazy('home')
        else:
            return reverse_lazy('accounts:email_verification')

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form)
