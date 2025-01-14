from django.contrib.auth import mixins
from django.shortcuts import redirect

from accounts.utils.email_verification import RedisDataStore


class LoginAndVerificationRequiredMixin(mixins.LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not request.user.is_email_verified:
            if RedisDataStore.is_expired(f'ev:{request.user.email}'):
                RedisDataStore.send_verification_code(request.user.email)
            return redirect('accounts:email_verification')
        return super().dispatch(request, *args, **kwargs)
