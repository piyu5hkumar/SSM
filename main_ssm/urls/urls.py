# django imports
from django.urls import path
from django.urls.resolvers import URLPattern

# additional imports
from ..views import (
    LoginUser,
    SignUp,
    UserProfileInfo,
    LogoutUser,
    CheckPassword,
    ChangePassword,
    ResetPassword,
    ForgotPassword,
    ForgotPasswordPage
)

urlpatterns = [
    # user and profile
    path('login', LoginUser.as_view()),
    path('logout', LogoutUser.as_view()),
    path('signup', SignUp.as_view()),
    path('user_profile', UserProfileInfo.as_view()),

    # password management
    path('check_password', CheckPassword.as_view()),
    path('change_password', ChangePassword.as_view()),
    path('reset_password', ResetPassword.as_view()),
    path('forgot_password', ForgotPassword.as_view()),
    path('reset_password/<uuid:uid>/<str:password_reset_token>', ForgotPasswordPage.as_view())
]
