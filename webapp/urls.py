# django imports
from django.urls import path
from .views import (
    Welcome,
    Login,
    SignUp,
    Profile,
    Account,
    Logout
)
from django.views.generic import TemplateView

from django.views import View
from django.shortcuts import HttpResponse

urlpatterns = [
    path('', Welcome.as_view(), name='welcome'),
    path('login', Login.as_view(), name='login'),
    path('signup', SignUp.as_view(), name='signup'),
    path('home', TemplateView.as_view(template_name='layouts/base_logged_in.html'), name='home'),
    path('invalid', TemplateView.as_view(template_name='layouts/error_page.html'), name='invalid'),

    # After you are logged in
    path('profile', Profile.as_view(), name='profile'),
    path('account', Account.as_view(), name='account'),
    path('logout', Logout.as_view(), name='logout')
]

# app_name = 'url_namespace_for_webapp'
# the above can be anything, but usually the app name itself is preferred
