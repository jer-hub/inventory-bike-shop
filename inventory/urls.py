from django.urls import path
from . import views

app_name = "inventory"
urlpatterns = [
    path('', views.view_main, name='view_main'),
    
    path('suppliers/', views.supplier_list, name='supplier_list'),
    path('suppliers/create/', views.create_supplier, name='create_supplier'),
    path('suppliers/update/<int:pk>/', views.update_supplier, name='update_supplier'),
    path('suppliers/delete/<int:pk>/', views.delete_supplier, name='delete_supplier'),
    
    path('products/', views.product_list, name='product_list'),
    path('products/create/', views.create_product, name='create_product'),
    path('products/update/<int:pk>/', views.update_product, name='update_product'),
    path('products/delete/<int:pk>/', views.delete_product, name='delete_product'),
    path('products/report/', views.products_showreport, name='products_report'),
]