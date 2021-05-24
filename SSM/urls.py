from django import urls
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(("webapp.urls", "webapp"), namespace="webapp_urls")),
    path("api/", include(("main_ssm.urls", "main_ssm"), namespace="api")),
]


"""
for reverse we need namespace:name or app_namespace:name (both are acceptable) 
and there are three ways to define namespace, and it can be done via include in the urlpatterns


1. include(module, namespace=None)

    -> Define your desired app_namespace in the correspoding app, for example in webapp.urls file I have
    defined one and commented it.

    -> Here module will be webapp.urls and namespace is the corresponding namespace to all the patterns in webapp.urls

2. include(pattern_list)

    -> here we directly define the pattern list(not webapp.urls, this format is used above and namespace=None in that case)
    but we can't give namespace here, to specify that, use the following approach

3. include((pattern_list/module, app_namespace), namespace=None)
    
    -> This approach is helpful, when we are working with a module 'X' which we don't want to modify(1st way isn't possible) or it is inaccessible, 
    you can't just write include("webapp.urls", namespace="webapp") because for this app_namespace had to be defined in the module 'X.urls',
    but what if doesn't?

    -> This approach not only assigns app_namespace but overrides the app_namespace in case one is provided in the 'X.urls'.
    It also gives namespace too.

DON'T FORGET: namespace:name or app_namespace:name (both are acceptable)
"""
