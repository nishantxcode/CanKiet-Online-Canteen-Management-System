
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index2, name='cankiet_index'),
    path('index2/',views.index2, name='index2'),
    path('login/',views.login, name='login'),
    path('orders/',views.orders, name='orders'),
    path('check/', views.login_check, name='check'),
    path('logout/', views.logout, name='logout'),
    path('canteens/', views.canteens, name='canteens'),
    path('<str:c_no>/menu/', views.menu, name='menu'),
    path('<str:c_no>/cart/', views.cart, name='cart'),
    # path('<str:c_no>/confirmation/', views.confirmation, name='confirmation'),
    path('<str:c_no>/food/', views.food, name='food'),
    path('galary/',views.galary,name='galary'),
    path('<str:c_no>/pay/',views.start_payment, name='start_payment'),
    path('verify_payment/', views.verify_payment, name='verify_payment'),
]