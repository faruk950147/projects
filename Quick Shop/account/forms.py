import threading
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm

User = get_user_model()
from account.models import Profile
"""
Profile form
"""
class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control', 'rows': '4', 'cols': '6'})
    class Meta:
        model = Profile
        fields = (
            '__all__'
        )
        exclude = ('user',)

""" 
Register form
"""
class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
            
    password = forms.CharField(
        max_length=150,
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )
    password1 = forms.CharField(
        max_length=150,
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'})
    )
    class Meta:
        model = User
        fields = (
            'username', 'email', 'password', 'password1',
        )
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
        }
        

    def clean_username(self):
        username = self.cleaned_data.get('username')
        model = self.Meta.model
        if model.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError('A user with the username already exists')
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        model = self.Meta.model
        if model.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('A user with the email already exists')
        return email

    def clean_password1(self, *args, **kwargs):
        password = self.cleaned_data.get('password')
        password1 = self.cleaned_data.get('password1')
        if password and password1 and password != password1:
                raise forms.ValidationError('Password Miss Matching')
        return password1
    
    #this method for save password
    def save(self, commit=True, *args, **kwargs):
        user = self.instance
        user.set_password(self.cleaned_data.get('password'))
        if commit:
            user.save()
        return user
""" 
Login form
"""
class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'Username or Email'})
    )
    password = forms.CharField(
        max_length=150,
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )
"""  
Change password form
"""
class ChangePasswordForm(forms.Form):
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})

    current_password = forms.CharField(
        max_length=150,
        widget=forms.PasswordInput(attrs={'placeholder': 'Current Password'})
    )
    new_password = forms.CharField(
        max_length=150,
        widget=forms.PasswordInput(attrs={'placeholder': 'New Password'})
    )
    new_password1 = forms.CharField(
        max_length=150,
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'})
    )

    def clean_current_password(self, *args, **kwargs):
        current_password = self.cleaned_data.get('current_password')

        if not self.user.check_password(current_password):
            raise forms.ValidationError("Incorrect Password")
        return current_password

    def clean_new_password(self, *args, **kwargs):
        new_password = self.cleaned_data.get('new_password')
        # why used self.data.get(new_password1) because no access new_password1 and this method for new_password
        new_password1 = self.data.get('new_password1')

        if new_password != new_password1:
            raise forms.ValidationError("Password Miss Matching")
        return new_password
""" 
Send email form
"""
class SendEmailForm(PasswordResetForm, threading.Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        threading.Thread.__init__(self)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
            
    def clean_email(self):
        if not User.objects.filter(email__iexact=self.cleaned_data.get('email')).exists():
            raise forms.ValidationError('The email is not registered')
        return self.cleaned_data.get('email')            

    def run(self) -> None:
        return super().send_mail(
        self.subject_template_name,
        self.email_template_name,
        self.context,
        self.from_email,
        self.to_email,
        self.html_email_template_name,
        )

    def send_mail(self, subject_template_name, email_template_name, context, from_email, to_email, html_email_template_name):
        self.subject_template_name=subject_template_name
        self.email_template_name=email_template_name
        self.context=context
        self.from_email=from_email
        self.to_email=to_email
        self.html_email_template_name=html_email_template_name
        self.start()
""" 
Reset password confirm form
"""    
class ResetPasswordConfirmForm(forms.Form):
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})

    new_password = forms.CharField(
        max_length=150,
        widget=forms.PasswordInput(attrs={'placeholder': 'New Password'})
    )
    new_password1 = forms.CharField(
        max_length=150,
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'})
    )

    def clean_new_password(self, *args, **kwargs):
        new_password = self.cleaned_data.get('new_password')
        # why used self.data.get(new_password1) because no access new_password1 and this method for new_password
        new_password1 = self.data.get('new_password1')
        if new_password and new_password1:
            if new_password != new_password1:
                raise forms.ValidationError("Password Miss Matching")

        return new_password
    
    def save(self, commit=True, *args, **kwargs):
        self.user.set_password(self.cleaned_data.get('new_password'))
        if commit:
            self.user.save()
        return self.user