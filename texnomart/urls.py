from django.urls import path
from .views import (
    AllProductsView, AllCategoriesView, CategoryProductsView, AddCategoryView,
    DeleteCategoryView, EditCategoryView, ProductDetailView,
    AttributeKeyView, AttributeValueView, AddProductView, EditProductView, DeleteProductView
)

urlpatterns = [
    path('texnomart-uz/', AllProductsView.as_view(), name='all-products'),
    path('texnomart-uz/categories/', AllCategoriesView.as_view(), name='all-categories'),
    path('texnomart-uz/category/<slug:category_slug>/', CategoryProductsView.as_view(), name='category-products'),
    path('texnomart-uz/categories/add-category/', AddCategoryView.as_view(), name='add-category'),
    path('texnomart-uz/category/<slug:category_slug>/delete/', DeleteCategoryView.as_view(), name='delete-category'),
    path('texnomart-uz/category/<slug:category_slug>/edit/', EditCategoryView.as_view(), name='edit-category'),
    path('texnomart-uz/product/detail/<int:product_id>/', ProductDetailView.as_view(), name='product-detail'),
    path('texnomart-uz/product/add-product/', AddProductView.as_view(), name='add-product'),
    path('texnomart-uz/product/<int:product_id>/edit/', EditProductView.as_view(), name='edit-product'),
    path('texnomart-uz/product/<int:product_id>/delete/', DeleteProductView.as_view(), name='delete-product'),
    path('texnomart-uz/attribute-key/', AttributeKeyView.as_view(), name='attribute-keys'),
    path('texnomart-uz/attribute-value/', AttributeValueView.as_view(), name='attribute-values'),
]
