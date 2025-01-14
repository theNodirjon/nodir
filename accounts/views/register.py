from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic import FormView

from accounts.forms import UserRegistrationForm
from accounts.utils.email_verification import RedisDataStore


class RegisterFormView(FormView):
    form_class = UserRegistrationForm
    template_name = 'booksaw/auth/register.html'
    success_url = reverse_lazy('accounts:email_verification')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        RedisDataStore.send_verification_code(user.email)
        return super().form_valid(form)
