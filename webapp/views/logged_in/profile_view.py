from django.views import View
from django.shortcuts import render, HttpResponse, redirect
from ...authentication import verify_authentication
from django.views.generic import FormView
from ...forms import ProfileForm, AccountForm, PrivacyForm
from main_ssm.models import User, UserProfile
from datetime import datetime


class Profile(View):

    @verify_authentication
    def get(self, request):
        user = User.objects.get(uid=request.session['uid'])
        user_profile = user.user_profile

        context = {
            'form': ProfileForm(),
            'user': {
                'first_name': user_profile.first_name,
                'middle_name': user_profile.middle_name,
                'last_name': user_profile.last_name,
                'd_o_b': user_profile.d_o_b,
            },
            'selected_nav_link': 'profile'
        }
        x = str(datetime.strptime(str(user_profile.d_o_b), "%Y-%m-%d").date())
        return render(request, 'webapp/logged_in/profile.html', context)

    def post(self, request):
        form = ProfileForm(request.POST)
        user = User.objects.get(uid=request.session['uid'])
        user_profile = user.user_profile

        if form.is_valid():
            user_profile.first_name = form.cleaned_data['first_name']
            user_profile.middle_name = form.cleaned_data['middle_name']
            user_profile.last_name = form.cleaned_data['last_name']
            user_profile.d_o_b = form.cleaned_data['d_o_b']
            user_profile.save(update_fields=['first_name', 'middle_name', 'last_name', 'd_o_b'])
        else:
            print(form.errors)
        context = {
            'form': ProfileForm(),
            'user': {
                'first_name': user_profile.first_name,
                'middle_name': user_profile.middle_name,
                'last_name': user_profile.last_name,
                'd_o_b': user_profile.d_o_b
            },
            'selected_nav_link': 'profile'
        }
        return render(request, 'webapp/logged_in/profile.html', context)


class Account(View):

    @verify_authentication
    def get(self, request):
        user = User.objects.get(uid=request.session['uid'])
        user_profile = user.user_profile

        context = {
            'account_form': AccountForm(),
            'privacy_form': PrivacyForm(),
            'user': {
                'username': user_profile.username,
                'email': user.email,
            },
            'selected_nav_link': 'profile'
        }
        x = str(datetime.strptime(str(user_profile.d_o_b), "%Y-%m-%d").date())
        return render(request, 'webapp/logged_in/account.html', context)

    def post(self, request):
        form = AccountForm(request.POST)
        user = User.objects.get(uid=request.session['uid'])
        user_profile = user.user_profile

        if form.is_valid():
            user_profile.username = form.cleaned_data['username']
            user.email = form.cleaned_data['email']
            user_profile.save(update_fields=['username'])
            user.save(update_fields=['email'])
        else:
            print(form.errors)
        context = {
            'form': AccountForm(),
            'privacy_form': PrivacyForm(),
            'user': {
                'username': user_profile.username,
                'email': user.email,
            },
            'selected_nav_link': 'profile'
        }
        return render(request, 'webapp/logged_in/account.html', context)



class Logout(View):
    def get(self, request):
        request.session.flush()
        return redirect('webapp_urls:welcome')
