from django.urls import path
from django.urls.resolvers import URLPattern
from ..views import Test, LoginUser, SignUp

urlpatterns = [
    path('test',Test.as_view()),
    path('login', LoginUser.as_view()),
    path('signup', SignUp.as_view())
]