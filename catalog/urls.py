from django.views.decorators.cache import cache_page

from catalog.apps import CatalogConfig
from django.urls import path
from catalog.views import ProductListView, ContactsView, ProductDetailView, ProductCreateView, ProductUpdateView, \
    ProductDeleteView, CategoryListView

app_name = CatalogConfig.name

urlpatterns = [
    path('', ProductListView.as_view(), name='home'),
    path('product_form/', ProductCreateView.as_view(), name='product_create'),
    path('product_detail/<int:pk>/', cache_page(60)(ProductDetailView.as_view()), name='product_detail'),
    path('product_update/<int:pk>/', ProductUpdateView.as_view(), name='product_update'),
    path('product_delete/<int:pk>/', ProductDeleteView.as_view(), name='product_delete'),

    path('contacts/', ContactsView.as_view(), name='contacts'),

    path('categories/', CategoryListView.as_view(), name='categories')

]
