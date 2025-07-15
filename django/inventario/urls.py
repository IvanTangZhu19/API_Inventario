from django.urls import path
from . import views

urlpatterns = [
    path('', views.Products),
    path('<int:productID>/', views.ProductByID)
]