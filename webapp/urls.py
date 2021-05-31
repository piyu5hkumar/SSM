# django imports
from django.urls import path
from .views import Welcome, Login, SignUp
from django.views.generic import TemplateView
urlpatterns = [
    path("", Welcome.as_view(), name="home"),
    path("login", Login.as_view(), name="login"),
    path("signup", SignUp.as_view(), name="signup"),
]

# app_name = "url_namespace_for_webapp"
# the above can be anything, but usually the app name itself is preferred
