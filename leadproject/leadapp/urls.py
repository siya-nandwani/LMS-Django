
from django.urls import path
from . import views
from .views import get_products

urlpatterns = [
    path('api/products/', get_products),
    path('api/leads/', views.get_leads),
    path('api/regions/', views.get_regions),
    path('logout/',views.logout_user,name='logout'),
    path('api/leads/add/', views.add_lead_api, name='add_lead'),
    path('api/regions/add/', views.add_region_api, name='add_region'),
    path('api/products/add/',views.add_product_api,name='add_product'),

    path('', views.login_view, name='login'),
    path('home/', views.home, name='home'),
    path('register/',views.register,name='register'),
    # Product
    path('products/', views.product_list, name='product_list'),
    path('products/add/', views.add_product, name='add_product'),
    path('products/edit/<int:pk>/', views.edit_product, name='edit_product'),
    path('products/delete/<int:pk>/', views.delete_product, name='delete_product'),
    path('api/products/update/<int:pk>/', views.update_product_api, name='update_product_api'),
    path('api/products/delete/<int:pk>/', views.delete_product_api, name='delete_product_api'),

    # Region
    path('regions/', views.region_list, name='region_list'),
    path('regions/add/', views.add_region, name='add_region'),
    path('regions/edit/<int:pk>/', views.edit_region, name='edit_region'),
    path('regions/delete/<int:pk>/', views.delete_region, name='delete_region'),
    path('api/regions/update/<int:pk>/', views.update_region_api, name='update_region_api'),
    path('api/regions/delete/<int:pk>/', views.delete_region_api, name='delete_region_api'),

    # Lead APIs
    path('leads/', views.lead_list, name='lead_list'),
    path('leads/add/', views.add_lead, name='add_lead'),
    path('leads/edit/<int:pk>/', views.edit_lead, name='edit_lead'),
    path('leads/delete/<int:pk>/', views.delete_lead, name='delete_lead'),
    path('api/leads/update/<int:pk>/', views.update_lead_api, name='update_lead_api'),
    path('api/leads/delete/<int:pk>/', views.delete_lead_api, name='delete_lead_api'),
    
    path('products/upload/',views.upload_products,name='upload_products'),
]