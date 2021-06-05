from main_ssm.models import User
from django.contrib.auth.hashers import check_password
from django.shortcuts import redirect, render


def user_authentication(request, phone_number, password):
    try:
        user = User.objects.get(phone_number=phone_number)
        if check_password(password, user.password):
            user_profile = user.user_profile
            request.session['display_name'] = str(user_profile)
            request.session['uid'] = str(user.uid)
            request.session['is_authenticated'] = True
            request.session.user = user
            print(request.session.user)
            return True, 'User credentials were valid', user
        else:
            return False, 'user credentials were not valid', None
    except User.DoesNotExist:
        return False, 'Invalid user', None


def verify_authentication_welcome_page(func):
    def verifier(self, request, *args, **kwargs):
        is_authenticated = request.session.get('is_authenticated', None)
        if is_authenticated:

            if request.method == 'POST':

                error = {
                    'error': '403 Forbidden ;(',
                    'error_detail': 'The server understood the request but refuses to authorize it.',
                    'additional_info': 'Please try after sometime.',
                }
                return render(request, 'layouts/error_page.html', {'error': error})

            return redirect('webapp_urls:home')
        else:
            return func(self, request, *args, **kwargs)
    return verifier


def verify_authentication(func):
    def verifier(self, request, *args, **kwargs):
        is_authenticated = request.session.get('is_authenticated', None)
        if is_authenticated:
            return func(self, request, *args, **kwargs)
        else:
            return redirect('webapp_urls:welcome')
    return verifier
