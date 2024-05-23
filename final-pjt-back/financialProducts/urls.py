from django.urls import path
from .views import deposit_products, deposit_product_options, fetch_external_deposit_products, join_product
from . import views

urlpatterns = [
    path('deposit-products/', deposit_products, name='deposit-products'),
    path('deposit-products/<int:product_pk>/', views.deposit_product),
    path('deposit-products/<str:fin_prdt_cd>/options/', deposit_product_options, name='deposit-product-options'),
    path('fetch-external-deposit-products/', fetch_external_deposit_products, name='fetch-external-deposit-products'),
    path('api/v1/join-product/', views.join_product, name='join_product'),
    path('deposit-allproducts/', views.deposit_allproducts, name='deposit-allproducts'),
    path('delete-join-product/<int:product_id>/', views.delete_join_product, name='delete-join-product'),
]