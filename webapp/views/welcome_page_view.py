from django.shortcuts import render
from django.shortcuts import render, HttpResponse, redirect
from ..authentication import user_authentication, verify_authentication_welcome_page
from ..forms import LoginForm, SignUpForm
from django.views import View
from main_ssm.models import User
from django.db import IntegrityError

LOGIN_TEMPLATE = 'webapp/login.html'


class Welcome(View):

    @verify_authentication_welcome_page
    def get(self, request):
        # is_authenticated = request.session.get('is_authenticated', None)
        # if is_authenticated:
        #     return redirect('webapp_urls:home')
        # else:
        return render(request, 'webapp/welcome.html')


class Login(View):

    @verify_authentication_welcome_page
    def get(self, request):
        form = LoginForm()
        return render(request, 'webapp/login.html', {'form': form})

    @verify_authentication_welcome_page
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            is_authenticated, message, user = user_authentication(request, phone_number, password)
            if is_authenticated:
                return redirect('webapp_urls:home')

        return render(request, 'webapp/login.html')


class SignUp(View):
    @verify_authentication_welcome_page
    def get(self, request):
        form = SignUpForm()
        return render(request, 'webapp/signup.html', {'form': form})

    @verify_authentication_welcome_page
    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            try:
                User.objects.create(phone_number=phone_number, password=password)
                return render(request, 'webapp/signup_successful')
            except IntegrityError:
                error = {
                    'error': '500 Internal server error ;(',
                    'error_detail': 'The server encountered an unexpected condition that prevented it from fulfilling the request.',
                    'additional_info': 'Please try after sometime, we\'ll look into this matter.',
                    'go_to_login': True
                }
                return render(request, 'layouts/error_page.html', {'error': error})

        return render(request, 'webapp/signup.html', {'form': form})
