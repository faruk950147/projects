from django.views import generic
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect, HttpResponse
from django.db.models import Q
from account.mixins import LogoutRequiredMixin

from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetConfirmView
)

from account.forms import (
    RegisterForm, 
    LoginForm,
    ChangePasswordForm,
    SendEmailForm,
    ResetPasswordConfirmForm
)
from account.models import (
    Profile
)
User = get_user_model()

# Create your views here.
def Activated_Email(request, email_token):
    try:
        user = Profile.objects.get(email_token=email_token)
        user.is_email_verified = True
        user.save()
        messages.success(request, "Your account has activated!")
        return redirect('login')
    except Exception as e:
        return HttpResponse('Invalid email token')
    
@method_decorator(never_cache, name='dispatch')
class Register(LogoutRequiredMixin, generic.View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'account/register.html', {'form': form})
    
    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # username = request.POST.get('username')
            # email = request.POST.get('email')
            # password = request.POST.get('password')
            # password1 = request.POST.get('password1')
            # user = User.objects.create_user(username=username, email=email, password=password)
            # user.set_password(password)
            # user.save()
            messages.warning(request, "Your account register successfully And email has been send on email!")
            return HttpResponseRedirect(request.path_info)
        return render(request, 'account/register.html', {'form': form})
    
@method_decorator(never_cache, name='dispatch')
class Login(LogoutRequiredMixin, generic.View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'account/login.html', {'form': form})
    
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = User.objects.filter(Q(username__iexact=username) | Q(email__iexact=username))

            if not user.exists():
                messages.error(request, 'Invalid account')
                return HttpResponseRedirect(request.path_info)
            
            if not user[0].profiles.is_email_verified:
                messages.warning(request, 'Your account is not activated')
                return HttpResponseRedirect(request.path_info)  
            
            user = authenticate(request, username=username, password=password)              
            if user:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Your username or password invalid')
                return HttpResponseRedirect(request.path_info)
        return render(request, 'account/login.html', {'form': form})
    
class Logout(generic.View):
    def get(self, request):
        logout(request)
        return redirect('login')
    
@method_decorator(never_cache, name='dispatch')
class ChangePassword(LoginRequiredMixin, generic.FormView):
    template_name = 'account/change_password.html'
    form_class = ChangePasswordForm
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('login')

    def get_form_kwargs(self):
        context = super().get_form_kwargs()
        context['user'] = self.request.user
        return context

    def form_valid(self, form):
        user = self.request.user
        user.set_password(form.cleaned_data.get('new_password1'))
        user.save()
        messages.success(self.request, "Password changed Successfully !")
        return super().form_valid(form)

class SendEmailToResetPassword(PasswordResetView):
    template_name = 'account/password_reset.html'
    form_class = SendEmailForm

class ResetPasswordConfirm(PasswordResetConfirmView):
    template_name = 'account/password_reset_confirm.html'
    form_class = ResetPasswordConfirmForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        messages.success(self.request, "Password reset successfully !")
        return super().form_valid(form)