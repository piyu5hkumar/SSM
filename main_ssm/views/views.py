# django imports
from django.contrib.auth import login, logout
from django.contrib.auth.hashers import make_password, check_password

# rest_framework imports
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.authtoken.models import Token

# additional imports
from ..models import User
from ..serializers import UserSerializer, LonginUserSerializer
from ..permissions import checkCustomPermission, LoginCheckPermission
from ..components import CustomResponse


class Test(APIView):
    # permission_classes = [checkCustomPermission]
    # authentication_classes = [LoginCheckPermission]

    def get(self, request):
        print(request.user.phone_number)
        return Response({}, status=status.HTTP_200_OK)