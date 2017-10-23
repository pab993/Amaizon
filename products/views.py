from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import UserForm
from .models import Product
from django.contrib.auth.models import User

# Create your views here.


def login_page(request):
    if request.user.is_authenticated():
        products_list = Product.objects.all()
        paginator = Paginator(products_list, 4)
        page = request.GET.get('page')
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            products = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            products = paginator.page(paginator.num_pages)
        context = {"products": products}
        return render(request, 'products/index.html', context)
    else:
        return render(request, 'products/login_page.html')


def login_user(request):
    if request.user.is_authenticated():
        products_list = Product.objects.all().order_by('-pub_date')
        paginator = Paginator(products_list, 4)
        page = request.GET.get('page')
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            products = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            products = paginator.page(paginator.num_pages)
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
                    products_list = Product.objects.all().order_by('-pub_date')
                    paginator = Paginator(products_list, 4)
                    page = request.GET.get('page')
                    try:
                        products = paginator.page(page)
                    except PageNotAnInteger:
                        # If page is not an integer, deliver first page.
                        products = paginator.page(1)
                    except EmptyPage:
                        # If page is out of range (e.g. 9999), deliver last page of results.
                        products = paginator.page(paginator.num_pages)
                    context = {"products": products}
                    return render(request, 'products/index.html', context)
                else:
                    return render(request, 'products/login_page.html', {'error_message': 'Your account has been disabled'})
            else:
                return render(request, 'products/login_page.html', {'error_message': 'Invalid login'})
        return render(request, 'products/login_page.html')


def register(request):
    if request.user.is_authenticated():
        products_list = Product.objects.all().order_by('-pub_date')
        paginator = Paginator(products_list, 4)
        page = request.GET.get('page')
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            products = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            products = paginator.page(paginator.num_pages)
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
                    products = Product.objects.all().order_by('-pub_date')
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
        products_list = Product.objects.all().order_by('-pub_date')
        query = request.GET.get("q")
        if query:
            products_filtered = products_list.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query)
            ).distinct()
            paginator = Paginator(products_filtered, 4)
            page = request.GET.get('page')
            try:
                products = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                products = paginator.page(1)
            except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
                products = paginator.page(paginator.num_pages)
            context = {"products": products}
            return render(request, 'products/index.html', context)
        else:
            paginator = Paginator(products_list, 4)
            page = request.GET.get('page')
            try:
                products = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                products = paginator.page(1)
            except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
                products = paginator.page(paginator.num_pages)
            context = {"products": products}
            return render(request, 'products/index.html', context)


def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'products/login_page.html', context)


def profile(request):   # Aún sin acabar
    if request.user.is_authenticated:
        if not request.POST:
            q = request.user.id
            user = User.objects.get(pk=q)
            userForm = UserForm(instance=user)
            context = {"form": userForm}
            return render(request, 'products/profile.html', context)
    else:
        return render(request, 'products/login_page.html')
