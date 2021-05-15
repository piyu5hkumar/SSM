from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def test(request):
    context = {'name':'dev manush'}
    return render(request,'main_ssm/test.html', context=context)
    return HttpResponse('<H1>Hello world</H1>')
