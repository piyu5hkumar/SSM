from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.authentication import BasicAuthentication

class Test(APIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [BasicAuthentication]
    def get(self, request):
        res = {
            "Piyush":"Hello world this is Piyush Kumar"
        }
        return Response(res, status=status.HTTP_200_OK)
