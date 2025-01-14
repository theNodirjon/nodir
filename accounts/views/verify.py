from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views import View
from django.views.generic import TemplateView

from accounts.utils.email_verification import RedisDataStore


class VerifyEmailFormView(LoginRequiredMixin, TemplateView):
    template_name = 'booksaw/auth/verify_email.html'

    def get(self, request, *args, **kwargs):
        if self.request.user.is_email_verified:
            return redirect('home')
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        inputs = ['code1', 'code2', 'code3', 'code4', 'code5', 'code6']
        code = ''.join([request.POST.get(i) for i in inputs])
        if RedisDataStore.get_data(f'ev:{request.user.email}') == code:
            request.user.is_email_verified = True
            request.user.save()
            return redirect('home')
        else:
            messages.error(request, "Invalid verification code. Please try again.")
        return self.render_to_response(self.get_context_data())
