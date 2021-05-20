# django imports
from django.urls import path
from django.urls.resolvers import URLPattern

# additional imports
from ..views import Test, LoginUser, SignUp, UserProfileInfo, LogoutUser

urlpatterns = [
    path("test", Test.as_view()),
    path("login", LoginUser.as_view()),
    path("logout", LogoutUser.as_view()),
    path("signup", SignUp.as_view()),
    path("user_profile", UserProfileInfo.as_view()),
]
