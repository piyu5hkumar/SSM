# django imports
from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path("", TemplateView.as_view(template_name="layouts/base.html"), name="home"),
]

# app_name = "url_namespace_for_webapp"
# the above can be anything, but usually the app name itself is preferred
