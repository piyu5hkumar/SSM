from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied
from rest_framework.authtoken.models import Token

class checkCustomPermission(BasePermission):
    def has_permission(self, request, view):
        print("inside checkCustomPermission class")
        # print(request.user.phone_number)
        print("outside checkCustomPermission class")
        # return False
        raise PermissionDenied(
            {"data": "this is the data field", "error": "this is the error field"}
        )


class LoginCheckPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            current_user_token = Token.objects.get(user=request.user)
            raise PermissionDenied(
                {
                    "data": None,
                    "error": {
                        "message": "You are already logged in",
                        "token": current_user_token.key,
                    },
                }
            )
        return True
