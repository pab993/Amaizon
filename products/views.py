from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import UserForm, ProfileForm1, ProfileForm2, AssessmentForm, ControlPanelForm
from .models import Product, UserProfile, Assessment, User, Neighbours, ControlPanel
from django.contrib.auth.decorators import login_required, permission_required
import random, math
from django.db.models import Count

# Create your views here.


def login_page(request):
    if request.user.is_authenticated():                                         # Comprobamos si está logueado, en caso de que lo esté,
        userprofile = UserProfile.objects.get(user=request.user)
        #productsRandom = Product.objects.all().order_by('?').distinct()[:6]     # Nos redirige a la página principal junto con los productos.
        products_list = Product.objects.all().order_by('-pub_date')
        product_recomended = prediction(request.user)
        print(product_recomended)
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
        context = {"products": products, "userprofile": userprofile, "productsRandom": product_recomended}
        return render(request, 'products/index.html', context)
    else:                                                                        # Si no está logueado nos lleva a la vista de login
        return render(request, 'products/login_page.html')


def login_user(request):
    if request.user.is_authenticated():
        userprofile = UserProfile.objects.get(user=request.user)
        #productsRandom = Product.objects.all().order_by('?').distinct()[:6]
        products_list = Product.objects.all().order_by('-pub_date')
        product_recomended = prediction(request.user)
        print(product_recomended)
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
        context = {"products": products, "userprofile": userprofile, "productsRandom": product_recomended}
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
                    #productsRandom = Product.objects.all().order_by('?')[:6]
                    products_list = Product.objects.all().order_by('-pub_date')
                    product_recomended = prediction(request.user)
                    print(product_recomended)
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
                    context = {"products": products, "userprofile": userprofile, "productsRandom": product_recomended}
                    return render(request, 'products/index.html', context)
                else:
                    return render(request, 'products/login_page.html', {'error_message': 'Your account has been disabled'})
            else:
                return render(request, 'products/login_page.html', {'error_message': 'Invalid login'})
        return render(request, 'products/login_page.html')


def register(request):
    if request.user.is_authenticated():
        userprofile = UserProfile.objects.get(user=request.user)
        #productsRandom = Product.objects.all().order_by('?').distinct()[:6]
        products_list = Product.objects.all().order_by('-pub_date')
        product_recomended = prediction(request.user)
        print(product_recomended)
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
        context = {"products": products, "userprofile": userprofile, "productsRandom": product_recomended}
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
                    #productsRandom = Product.objects.all().order_by('?').distinct()[:6]
                    userprofile = UserProfile.objects.get(user=request.user)
                    product_recomended = prediction(user)
                    print(product_recomended)
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
                    context = {'products': products, 'userprofile': userprofile, "productsRandom": product_recomended}
                    return render(request, 'products/index.html', context)
        context.update({"form": form, "form2": form2, "form3": form3, 'form4': form4, 'form5': form5, 'form6': form6})
        return render(request, 'products/register.html', context)


def index(request):
    if not request.user.is_authenticated():
        return render(request, 'products/login_page.html')
    else:
        product_recomended = prediction(request.user)
        print(product_recomended)
        products_list = Product.objects.all().order_by('-pub_date')
        #productsRandom = Product.objects.all().order_by('?').distinct()[:6]
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
            context = {"products": products, "userprofile": userprofile, "productsRandom": product_recomended}
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
            context = {"products": products, "userprofile": userprofile, "productsRandom": product_recomended}
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
        paginator = Paginator(assessments_list, 5)
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


@login_required
@permission_required('is_superuser')
def control(request):
    context = {}
    user = request.user
    userprofile = UserProfile.objects.get(user=user)
    form = ControlPanelForm(request.POST or None, instance=ControlPanel.objects.all().first())
    if request.method == 'POST':
        if form.is_valid():
            controlPanel = form.save(commit=False)
            controlPanel.save()
        users_list = User.objects.all().exclude(id=user.id, is_superuser=True)                                                                 #Recuperamos la lista de todos los usuarios menos el del admin                                          #Recuperamos la lista de todos los productos
        cp = ControlPanel.objects.all().first()
        #products_list = Product.objects.annotate(ass_count=Count('assessment')).filter(ass_count__gte=cp.threshold)
        Neighbours.objects.all().delete()                                                                                   #Eliminamos todos los registros de similitudes anteriores
        for u1 in users_list:                                                                                               #Recorremos la lista de todos los usuarios para ir rellenado sus registros nuevos
            assessments1 = Assessment.objects.filter(user=u1)
            if assessments1:
                users_list2 = User.objects.all().exclude(id__in=[user.id, u1.id], is_superuser=True)                                           #Recuperamos la lista de usuarios pero ahora sin el usuario1
                total1 = 0
                for a1 in assessments1:                                                                                     #Calculo la media del usuario a tratar
                    total1 += a1.score
                avg1 = total1 / len(assessments1)
                total2 = 0
                for u2 in users_list2:
                    products_list_f = []
                    assessments2 = Assessment.objects.filter(user=u2)
                    if assessments2:
                        for a2 in assessments2:                                                                             # Calculo la media del siguiente usuario
                            total2 += a2.score
                        avg2 = total2 / len(assessments2)
                        productsU1 = []
                        productsU2 = []
                        for item1 in assessments1:                                                                          # Filtro los productos que ambos usuarios han puntuado
                            productsU1.append(item1.product)
                        for item2 in assessments2:
                            productsU2.append(item2.product)
                        for item in productsU1:
                            if item in productsU2:
                                products_list_f.append(item)                                                                # Podrían no tener productos en común ¡OJO!
                        numeradorTotal = 0.0
                        denominador1 = 0.0
                        denominador2 = 0.0
                        if products_list_f:                                                                                 # Combruebo si la lista está vacía
                            for p in products_list_f:                                                                       #Recorremos la lista de productos para aplicar el sumatorio
                                assessment1 = Assessment.objects.filter(user=u1, product=p).first()
                                if assessment1 is None:
                                    score1 = 0
                                else:
                                    score1 = assessment1.score
                                assessment2 = Assessment.objects.filter(user=u2, product=p).first()
                                if assessment2 is None:
                                    score2 = 0
                                else:
                                    score2 = assessment2.score
                                numerador1 = score1 - avg1
                                numerador2 = score2 - avg2
                                multNumerador = numerador1 * numerador2
                                numeradorTotal += multNumerador
                                denominador1 += (score1 - avg1) * (score1 - avg1)
                                denominador2 += (score2 - avg2) * (score2 - avg2)
                            denominadorTotal1 = math.sqrt(denominador1)
                            denominadorTotal2 = math.sqrt(denominador2)
                            if numeradorTotal == 0 or denominadorTotal1 == 0 or denominadorTotal2 == 0:
                                similitud = 0
                            else:
                                similitud = numeradorTotal / (denominadorTotal1 * denominadorTotal2)
                            if similitud >= cp.threshold:
                                neighbour = Neighbours.objects.create(user=u1, idUser=u2.id, sim=similitud)
                                neighbour.save()
        context.update({'success': 'Operation carried out successfully'})
    context.update({'user': user, 'userprofile': userprofile, 'form': form})
    return render(request, 'products/controlPanel.html', context)


# LLamadas a otros metodos suplementarios
# ========================================================================================================

def prediction(u):
    #Declaro las variables
    products_list_full = Product.objects.all()                                                                             #Todos los productos
    products_no_reviewed = []                                                                                              #Todos los productos que el usuario no ha puntuado
    #Calculo la media del usuario logueado
    assessments = Assessment.objects.filter(user=u)
    avg = average(assessments)
    #Filtro a sólo los productos que no ha puntuado el usuario
    for p in products_list_full:                                                                                           #¿Pongo aquí otro filtro para los productos que cumplan con el mínimo umbral?
        assessment = Assessment.objects.filter(user=u, product=p).first()
        if assessment is None:
            products_no_reviewed.append(p)
    #Aquí empieza la predicción
    vecinos = Neighbours.objects.filter(user=u)                                                                             # Recupero los vecinos del usuario logueado
    if vecinos and products_no_reviewed:
        products_predictions = {}
        for p2 in products_no_reviewed:                                                                                     # Recorro los productos que no he puntuado
            prediccion = 0.0
            totalNumerador = 0.0
            totalDenominador = 0.0
            for v in vecinos:                                                                                               # Recorro a mis vecinos semejantes
                assessments2 = Assessment.objects.filter(user_id=v.idUser)
                avg2 = average(assessments2)
                userVecino = User.objects.get(pk=v.idUser)
                assessment2 = Assessment.objects.filter(user=userVecino, product=p2).first()                            #Aquí miro que el producto que no he valorado sí haya sido valorado por mi vecino
                if assessment2:
                    totalNumerador += v.sim * (assessment2.score - avg2)
                    totalDenominador += v.sim
            if totalDenominador != 0:
                prediccion = avg + (totalNumerador / totalDenominador)
                products_predictions[p2] = prediccion
        if products_predictions:
            all_products_recommended_sorted = sorted(products_predictions, key=products_predictions.__getitem__,
                                                     reverse=True)[:3]
            return all_products_recommended_sorted


def average(assessments):
    total = 0
    for a in assessments:
        total += a.score
    if total == 0:
        avg = 0
    else:
        avg = total / len(assessments)
    return avg

