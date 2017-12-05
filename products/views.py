from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import UserForm, ProfileForm1, ProfileForm2, AssessmentForm
from .models import Product, UserProfile, Assessment

# Create your views here.


def login_page(request):
    if request.user.is_authenticated():                                         # Comprobamos si está logueado, en caso de que lo esté,
        userprofile = UserProfile.objects.get(user=request.user)
        productsRandom = Product.objects.all().order_by('?').distinct()[:6]     # Nos redirige a la página principal junto con los productos.
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
        context = {"products": products, "userprofile": userprofile, "productsRandom": productsRandom}
        return render(request, 'products/index.html', context)
    else:                                                                        # Si no está logueado nos lleva a la vista de login
        return render(request, 'products/login_page.html')


def login_user(request):
    if request.user.is_authenticated():
        userprofile = UserProfile.objects.get(user=request.user)
        productsRandom = Product.objects.all().order_by('?').distinct()[:6]
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
        context = {"products": products, "userprofile": userprofile, "productsRandom": productsRandom}
        return render(request, 'products/index.html', context)
    else:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    userprofile = UserProfile.objects.get(user=user)
                    productsRandom = Product.objects.all().order_by('?')[:6]
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
                    context = {"products": products, "userprofile": userprofile, "productsRandom": productsRandom}
                    return render(request, 'products/index.html', context)
                else:
                    return render(request, 'products/login_page.html', {'error_message': 'Your account has been disabled'})
            else:
                return render(request, 'products/login_page.html', {'error_message': 'Invalid login'})
        return render(request, 'products/login_page.html')


def register(request):
    if request.user.is_authenticated():
        userprofile = UserProfile.objects.get(user=request.user)
        productsRandom = Product.objects.all().order_by('?').distinct()[:6]
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
        context = {"products": products, "userprofile": userprofile, "productsRandom": productsRandom}
        return render(request, 'products/index.html', context)
    else:
        form = UserForm(request.POST or None)
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            #email = form.cleaned_data['email']
            user.set_password(password)
            user.save()
            user_profile = UserProfile(user=user)
            user_profile.save()
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    products_list = Product.objects.all().order_by('-pub_date')
                    productsRandom = Product.objects.all().order_by('?').distinct()[:6]
                    userprofile = UserProfile.objects.get(user=request.user)
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
                    context = {'products': products, 'userprofile': userprofile, "productsRandom": productsRandom}
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
        productsRandom = Product.objects.all().order_by('?').distinct()[:6]
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
            userprofile = UserProfile.objects.get(user=request.user)
            context = {"products": products, "userprofile": userprofile, "productsRandom": productsRandom}
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
            userprofile = UserProfile.objects.get(user=request.user)
            context = {"products": products, "userprofile": userprofile, "productsRandom": productsRandom}
            return render(request, 'products/index.html', context)


def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'products/login_page.html', context)


def profile(request):
    if request.user.is_authenticated:
        userprofile = UserProfile.objects.get(user=request.user)
        if request.method == "POST":
            form = ProfileForm1(request.POST, instance=request.user)
            form2 = ProfileForm2(request.POST, request.FILES or None, instance=userprofile)
            if form.is_valid():
                user = form.save(commit=False)
                user.save()
                if form2.is_valid():
                    userprofile = form2.save(commit=False)
                    userprofile.save()
                    return redirect('index')

        else:
            form = ProfileForm1(instance=request.user)
            form2 = ProfileForm2(instance=userprofile)
        context = {"form": form,
                   "form2": form2,
                   "userprofile": userprofile}
        return render(request, 'products/profile.html', context)
    else:
        return render(request, 'products/login_page.html')


def detail(request, product_id):
    if not request.user.is_authenticated():
        return render(request, 'products/login_page.html')
    else:
        user = request.user
        product = get_object_or_404(Product, pk=product_id)
        userprofile = UserProfile.objects.get(user=user)
        assessments_list = Assessment.objects.filter(product=product_id).order_by('-post_date')
        exist_assessment = Assessment.objects.filter(product=product_id, user=user)
        paginator = Paginator(assessments_list, 10)
        form = AssessmentForm(request.POST or None)
        if request.method == 'POST':
            if form.is_valid():
                assessment = form.save(commit=False)
                assessment.product = product
                assessment.user = user
                assessment.save()
        page = request.GET.get('page')
        try:
            assessments = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            assessments = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            assessments = paginator.page(paginator.num_pages)
        return render(request, 'products/detail.html', {'product': product, 'user': user, 'userprofile': userprofile,
                                                        'assessments': assessments, 'form': form,
                                                        'exist_assessment': exist_assessment})
