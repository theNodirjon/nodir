from django.urls import path

from accounts.views import AuthFormView, RegisterFormView, VerifyEmailFormView

urlpatterns = [
    path('login/', AuthFormView.as_view(), name='login'),
    path('register/', RegisterFormView.as_view(), name='register'),
    path('verification/', VerifyEmailFormView.as_view(), name='email_verification'),
]
