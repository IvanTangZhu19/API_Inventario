from django.urls import path
from . import views

urlpatterns = [
    path('inventory/', views.Products),
    path('inventory/<int:productID>/', views.ProductByID),
    path('users/login/', views.login)
]