from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from . import models
from . import forms
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from .serializers import ProductSerialize
from rest_framework.decorators import api_view
from rest_framework.views import Response
from django.views import generic
from django.contrib.auth.decorators import login_required


def Home(request):
    products = models.Product.objects.filter(available=True)
    categories = models.Category.objects.filter(active=True)
    context = {"products": products, "categories": categories}
    return render(request, "app/home.html", context)


def Search(request):
    q = request.GET["q"]
    products = models.Product.objects.filter(available=True, name__icontains=q)
    categories = models.Category.objects.filter(active=True)
    context = {"products": products,
               "categories": categories,
               "title": q + " - search"}
    return render(request, "app/list.html", context)



def categories(request, slug):
    cat = models.Category.objects.get(slug=slug)
    products = models.Product.objects.filter(available=True, category=cat)
    categories = models.Category.objects.filter(active=True)
    context = {"products":products, "categories":categories, "title":cat.name + " - Categories"}
    return render(request, "app/list.html", context)

@login_required(login_url='app:signup')
def Detail(request, slug):
    product = models.Product.objects.get(available=True, slug=slug)
    if request.method == "POST":
        form = forms.ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            messages.success(request, "Review saved")
        else:
            messages.error(request, "Invalid form")
    else:
        form = forms.ReviewForm()


    categories = models.Category.objects.filter(active=True)
    context = {"product" : product,
               "categories":categories,
               "form": form}
    return render(request, "app/detail.html", context)

def Cart(request,slug):
    product = models.Product.objects.get(available=True,slug=slug)
    initial ={"item":[],"price":0.0,"count":0}
    session = request.session.get("data",initial)
    if slug in session["item"]:
        messages.success(request,"Already exists in cart!")
    else:
        session["item"].append(slug)
        session["price"]+=float(product.price)
        session["count"]+=1
        request.session["data"]=session
        messages.success(request,"Added Successfully!")
    return redirect('app:detail',slug)


def MyCart(request):
    sess = request.session.get("data", {"item":[]})
    products = models.Product.objects.filter(available=True, slug__in=sess["item"])
    categories = models.Category.objects.filter(active=True)
    context = {"products": products,
               "categories": categories,
               "title": "My Cart"}
    return render(request, "app/list.html", context)



def SignUpView(request):
    if request.method == "POST":
        form = forms.SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            messages.success(request, "User saved")
            return redirect("app:signin")
        else:
            messages.error(request, "Error in form")
    else:
        form = forms.SignUpForm()
    context = {"form": form}
    return render(request, "app/signup.html", context)

def SignInView(request):
    if request.method == 'POST':
        form = forms.SignInForm(request.POST)
        if form.is_valid():
            username = form["username"].value()
            password = form["password"].value()
            user = authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                messages.success(request,'Successfully Logged In')
                return redirect('app:home')
            else:
                messages.warning(request,"Invalid Username or Password")
    else:
        form = forms.SignInForm()
    return render(request,'app/signin.html',{'form':form})

def SignOutView(request):
    logout(request)
    return redirect('app:signin')

@api_view(['GET'])
def api_product(request):
    query = request.GET.get('q','')
    product = models.Product.objects.filter(Q(name__icontains=query) | Q(product_detail__icontains=query))
    serialize = ProductSerialize(product,many=True)
    return Response(serialize.data)
