from django.shortcuts import render
from django.shortcuts import render, HttpResponse, redirect
from ..authentication import user_authentication, verify_authentication_welcome_page
from ..forms import LoginForm, SignUpForm
from django.views import View
from main_ssm.models import User
from django.db import IntegrityError

LOGIN_TEMPLATE = 'webapp/welcome_page/login.html'


class Welcome(View):

    @verify_authentication_welcome_page
    def get(self, request):
        # is_authenticated = request.session.get('is_authenticated', None)
        # if is_authenticated:
        #     return redirect('webapp_urls:home')
        # else:
        return render(request, 'webapp/welcome_page/welcome.html')


class Login(View):

    @verify_authentication_welcome_page
    def get(self, request):
        form = LoginForm()
        return render(request, 'webapp/welcome_page/login.html', {'form': form})

    @verify_authentication_welcome_page
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            is_authenticated, message, user = user_authentication(request, phone_number, password)
            if is_authenticated:
                return redirect('webapp_urls:home')

        return render(request, 'webapp/welcome_page/login.html')


class SignUp(View):
    @verify_authentication_welcome_page
    def get(self, request):
        form = SignUpForm()
        return render(request, 'webapp/welcome_page/signup.html', {'form': form})

    @verify_authentication_welcome_page
    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            try:
                User.objects.create(phone_number=phone_number, password=password)
                return render(request, 'webapp/welcome_page/signup_successful.html')
            except IntegrityError:
                context = {
                    'form': form,
                    'error': {
                        'integrity_error': True,
                        'error_detail': 'This User already exists'
                    }
                }
                return render(request, 'webapp/welcome_page/signup.html', context)
        context = {
            'form': SignUpForm(),
            'error': {
                'validation_error': True,
                'error_detail': ''
            }
        }
        return render(request, 'webapp/welcome_page/signup.html', context)
