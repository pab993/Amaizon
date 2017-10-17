from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.template import loader
from .forms import ProductForm, AssessmentForm, UserForm
from .models import Product

# Create your views here.


def login_page(request):
    if request.user.is_authenticated():
        products = Product.objects.all()
        context = {"products": products}
        return render(request, 'products/index.html', context)
    else:
        return render(request, 'products/login_page.html')


def login_user(request):
    if request.user.is_authenticated():
        products = Product.objects.all()
        context = {"products": products}
        return render(request, 'products/index.html', context)
    else:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    products = Product.objects.all()
                    context = {"products": products}
                    return render(request, 'products/index.html', context)
                else:
                    return render(request, 'products/login_page.html', {'error_message': 'Your account has been disabled'})
            else:
                return render(request, 'products/login_page.html', {'error_message': 'Invalid login'})
        return render(request, 'products/login_page.html')


def register(request):
    if request.user.is_authenticated():
        products = Product.objects.all()
        context = {"products": products}
        return render(request, 'products/index.html', context)
    else:
        form = UserForm(request.POST or None)
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            user.set_password(password)
            user.save()
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    products = Product.objects.all()
                    context = {'products': products}
                    return render(request, 'products/index.html', context)
        context = {
            "form": form,
        }
        return render(request, 'products/register.html', context)


def index(request):
    if not request.user.is_authenticated():
        return render(request, 'products/login_page.html')
    else:
        products = Product.objects.all()
        context = {"products": products}
        return render(request, 'products/index.html', context)


def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'products/login_page.html', context)