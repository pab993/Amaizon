from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import UserForm, ProfileForm1, ProfileForm2, AssessmentForm
from .models import Product, UserProfile, Assessment
import random

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
        context = {}
        if request.method == "POST":
            form2 = AssessmentForm(request.POST, prefix='Review1')
            form3 = AssessmentForm(request.POST, prefix='Review2')
            form4 = AssessmentForm(request.POST, prefix='Review3')
            form5 = AssessmentForm(request.POST, prefix='Review4')
            form6 = AssessmentForm(request.POST, prefix='Review5')
            product0 = Product.objects.get(pk=request.POST.get('Review1-product'))
            product1 = Product.objects.get(pk=request.POST.get('Review2-product'))
            product2 = Product.objects.get(pk=request.POST.get('Review3-product'))
            product3 = Product.objects.get(pk=request.POST.get('Review4-product'))
            product4 = Product.objects.get(pk=request.POST.get('Review5-product'))
            context.update({'products_form_0': product0, 'products_form_1': product1, 'products_form_2': product2,
                            'products_form_3': product3, 'products_form_4': product4,
                            'error_message': 'The registration could not be completed. Please check that all fields have been filled in correctly.'})
        else:
            my_ids = Product.objects.values_list('id', flat=True)
            n = 5
            rand_ids = random.sample(list(my_ids), n)
            products_form = Product.objects.filter(id__in=rand_ids)
            form2 = AssessmentForm(initial={'product': products_form[0]}, prefix='Review1')
            form3 = AssessmentForm(initial={'product': products_form[1]}, prefix='Review2')
            form4 = AssessmentForm(initial={'product': products_form[2]}, prefix='Review3')
            form5 = AssessmentForm(initial={'product': products_form[3]}, prefix='Review4')
            form6 = AssessmentForm(initial={'product': products_form[4]}, prefix='Review5')
            context.update({'products_form_0': products_form[0], 'products_form_1': products_form[1], 'products_form_2': products_form[2], 'products_form_3': products_form[3], 'products_form_4': products_form[4]})
        form = UserForm(request.POST or None)
        if form.is_valid() and form2.is_valid() and form3.is_valid() and form4.is_valid() and form5.is_valid() and form6.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            user_profile = UserProfile(user=user)
            user_profile.save()
            assessment0 = form2.save(commit=False)
            assessment1 = form3.save(commit=False)
            assessment2 = form4.save(commit=False)
            assessment3 = form5.save(commit=False)
            assessment4 = form6.save(commit=False)
            product0 = form2.cleaned_data['product']
            product1 = form3.cleaned_data['product']
            product2 = form4.cleaned_data['product']
            product3 = form5.cleaned_data['product']
            product4 = form6.cleaned_data['product']
            context.update({'products_form_0': product0, 'product_form_1': product1, 'products_form_2': product2, 'products_form_3': product3, 'products_form_4': product4})
            assessment0.user = user
            assessment0.save()
            assessment1.user = user
            assessment1.save()
            assessment2.user = user
            assessment2.save()
            assessment3.user = user
            assessment3.save()
            assessment4.user = user
            assessment4.save()
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
        context.update({"form": form, "form2": form2, "form3": form3, 'form4': form4, 'form5': form5, 'form6': form6})
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
        exist_assessment = Assessment.objects.filter(product=product_id, user=user).first()
        paginator = Paginator(assessments_list, 10)
        form = AssessmentForm(request.POST or None, instance=exist_assessment)
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
