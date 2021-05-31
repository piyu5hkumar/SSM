from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.shortcuts import render, HttpResponse

from ..forms import LoginForm, SignUpForm


class Welcome(TemplateView):
    template_name = 'webapp/welcome.html'


class Login(FormView):
    template_name = 'webapp/login.html'
    form_class = LoginForm
    success_url = 'login'

    def post(self, request):
        return render(request, 'layouts/base_signed_in.html')


class SignUp(FormView):
    template_name = 'webapp/signup.html'
    form_class = SignUpForm
    success_url = 'signup'

    def post(self, request):
        return HttpResponse('okkkkkkkkkkkkkkkk signup')
