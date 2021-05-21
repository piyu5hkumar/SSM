# django imports
from django.urls import path
from django.urls.resolvers import URLPattern

# additional imports
from ..views import (
    Test,
    LoginUser,
    SignUp,
    UserProfileInfo,
    LogoutUser,
    CheckPassword,
    ResetPassword,
)

urlpatterns = [
    # user and profile
    path("test", Test.as_view()),
    path("login", LoginUser.as_view()),
    path("logout", LogoutUser.as_view()),
    path("signup", SignUp.as_view()),
    path("user_profile", UserProfileInfo.as_view()),
    # password management
    path("check_password", CheckPassword.as_view()),
    path("reset_password", ResetPassword.as_view()),
]
