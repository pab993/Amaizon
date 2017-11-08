from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.

def index(request):
    #return render(request, "login_page.html")
    return HttpResponse("<h1>Test</h1>")
