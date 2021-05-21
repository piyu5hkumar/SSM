from rest_framework.views import APIView
from ..components import CustomResponse
from ..serializers import PasswordSerializer, ResetPasswordSerializer
from django.contrib.auth.hashers import check_password, make_password
from rest_framework.response import Response
from rest_framework import status


class CheckPassword(APIView):
    def post(self, request):
        resp = CustomResponse()
        serializer = PasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = serializer.validated_data.get("password", "")
        if check_password(password, request.user.password):
            resp.add_data_field(message="Password matched successfully")
        else:
            resp.add_error_field(message="Password didn't match")
        return Response(resp.get_response(), status=status.HTTP_200_OK)


class ResetPassword(APIView):
    def post(self, request):
        resp = CustomResponse()
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        old_password = serializer.validated_data.get("old_password", "")
        if check_password(old_password, request.user.password):
            new_password = serializer.validated_data.get("new_password", "")
            request.user.password = new_password
            request.user.save(update_fields=["password"])
            resp.add_data_field(message="Password successfully reset")
        else:
            resp.add_error_field(message="Please enter correct current password")
        return Response(resp.get_response(), status=status.HTTP_200_OK)


class ForgotPassword(APIView):
    pass
