from django.shortcuts import render

from django.http import HttpResponse


# Create your views here.

def home(request):
    return HttpResponse("Hello world !")


def home_template(request):
    return render(request, 'home_template.html')


def home_template_dynamic(request):
    return render(request, 'home_template_dy.html', {'name': 'Ajithkumar-M'})

def add(request):
    val1=int(request.GET['num1'])
    val2=int(request.GET['num2'])
    data=val1+val2
    return render(request, 'result.html',{'data':data})
