from django.urls import path
from account.views import (
    Register, Login, Logout, ChangePassword, SendEmailToResetPassword, ResetPasswordConfirm, Activated_Email
)
from django.contrib.auth.views import (
    PasswordResetDoneView,
    PasswordResetCompleteView
)

urlpatterns = [
    path('register/', Register.as_view(), name='register'),
    path('login/', Login.as_view(), name='login'),
    path('activated/<email_token>/', Activated_Email, name='activated'),
    path('logout/', Logout.as_view(), name='logout'),
    path('change_password/', ChangePassword.as_view(), name='change_password'),
    path('password_reset/', SendEmailToResetPassword.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(template_name='account/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', ResetPasswordConfirm.as_view(), name='password_reset_confirm'),
]
