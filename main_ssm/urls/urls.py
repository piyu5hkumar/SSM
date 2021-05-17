from django.urls import path
from django.urls.resolvers import URLPattern
from ..views import Test

urlpatterns = [
    path('kill',Test.as_view())
]