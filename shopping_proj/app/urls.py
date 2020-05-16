from django.urls import path,re_path
from . import views


app_name = 'app'

urlpatterns = [
    path('',views.Home,name="home"),
    path('signup/',views.SignUpView,name="signup"),
    path('signin/',views.SignInView,name="signin"),
    path('signout/',views.SignOutView,name="signout"),
    path('search/',views.Search,name="search"),
    path('detail/<slug>/',views.Detail,name="detail"),
    path('api/products/', views.api_product, name="api_product"),
    path('categories/<slug>/', views.categories, name="categories"),
    path('<slug>/cart/', views.Cart, name="cart"),
    path('mycart/', views.MyCart, name="mycart"),
    path('api/products/', views.api_product, name="api_products"),
   # re_path('signup/',views.SignUpView,name=signup"")

]