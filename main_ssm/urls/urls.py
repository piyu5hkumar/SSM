from django.urls import path
from django.urls.resolvers import URLPattern
from ..views import Test, LoginUser

urlpatterns = [
    path('kill',Test.as_view()),
    path('login', LoginUser.as_view())
]