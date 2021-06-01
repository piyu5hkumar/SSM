# django imports
from django.urls import path
from .views import Welcome, Login, SignUp
from django.views.generic import TemplateView
urlpatterns = [
    path('', Welcome.as_view(), name='welcome'),
    path('login', Login.as_view(), name='login'),
    path('signup', SignUp.as_view(), name='signup'),
    path('home', TemplateView.as_view(template_name='layouts/base_logged_in.html'), name='home'),
    path('invalid', TemplateView.as_view(template_name='layouts/error_page.html'), name='invalid')
]

# app_name = 'url_namespace_for_webapp'
# the above can be anything, but usually the app name itself is preferred
