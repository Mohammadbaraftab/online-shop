from django.shortcuts import render, redirect
from django.views import View
from .forms import UserRegistrationForm, VerifyCodeForm
from utils import send_otp_code
from .models import OtpCode, User
import random
from django.contrib import messages


class UserRegisterView(View):
    form_class = UserRegistrationForm
    template_name = "accounts/register.html"

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"form":form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            random_code = random.randint(1000, 9999)
            send_otp_code(form.cleaned_data["phone_number"], code=random_code)
            OtpCode.objects.create(phone_number = form.cleaned_data["phone_number"], code = random_code)
            request.session["user_registration_info"] = {
                "phone_number": form.cleaned_data["phone_number"],
                "email" : form.cleaned_data["email"],
                "full_name" : form.cleaned_data["full_name"],
                "password" : form.cleaned_data["password"]
            }
            messages.success(request, "we sent you a code", extra_tags="success")
            return redirect("accounts:verify_code")
        return render(request, self.template_name, {"form":form})
    

class UserRegisterVerifyCodeView(View):
    form_class = VerifyCodeForm
    template_name = "accounts/verify.html"

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {"form":form})

    def post(self, request):
        user_session = request.session["user_registration_info"]
        code_instance = OtpCode.objects.get(phone_number = user_session["phone_number"])
        form = self.form_class(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            if cleaned_data["code"] == code_instance.code:
                User.objects.create_user(
                                        phone_number = user_session["phone_number"],
                                        email = user_session["email"],
                                        full_name = user_session["full_name"],
                                        password = user_session["password"]
                )
                messages.success(request, "You registered successfully", extra_tags="success")
                code_instance.delete()
                return redirect("home:home")
            else:
                messages.error(request, "This code is wrong", extra_tags="danger")
                return redirect("accounts:verify_code")
        return render(request, self.template_name, {"form":form})