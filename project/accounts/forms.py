from django import forms
from django.core.exceptions import ValidationError
from .models import User, OtpCode
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput) 

    class Meta:
        model = User
        fields = ("phone_number", "email", "full_name")

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords must match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(label=("Password"), 
                    help_text = ("Raw passwords are not stored, so there is no way to see "
                    "this user's password, but you can change the password "
                    "using <a href=\"../password/\">this form</a>."))
    class Meta:
        model = User
        fields = ("phone_number", "email", "full_name", "password")


class UserRegistrationForm(forms.Form):
    email = forms.EmailField()
    full_name = forms.CharField(label= "full name", max_length=100)
    phone_number = forms.CharField(label="phone number", max_length=11)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email = email).exists():
            raise ValidationError("This email already exist")
        return email
    
    def clean_phone(self):
        phone = self.cleaned_data["phone_number"]
        if User.objects.filter(phone_number = phone).exists():
            raise ValidationError("This phone number already exist")
        OtpCode.objects.filter(phone_number = phone).delete()
        return phone



class VerifyCodeForm(forms.Form):
    code = forms.IntegerField()


class UserLoginForm(forms.Form):
    phone_number = forms.CharField(label="Phone Number", max_length=11)
    password = forms.CharField(widget=forms.PasswordInput)