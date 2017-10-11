from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.template import loader
from django.http import HttpResponse
from .forms import ProductForm, AssessmentForm, UserForm

# Create your views here.


def index(request):
    return render(request, 'products/index.html')


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return render(request, 'logged.html')
            else:
                return render(request, 'products/index.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'products/index.html', {'error_message': 'Invalid login'})
    return render(request, 'products/index.html')


def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
#        user = authenticate(username=username, password=password)
        if user is not None:
            return render(request, 'products/index.html')
    context = {
        "form": form,
    }
    return render(request, 'products/register.html', context)

