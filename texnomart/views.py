from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.core.cache import cache
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, RetrieveAPIView, ListAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Product, Category, AttributeKey, AttributeValue
from .serializers import ProductSerializer, CategorySerializer, AttributeKeySerializer, AttributeValueSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


class AllProductsView(ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        cache_key = 'all_products'
        products = cache.get(cache_key)
        if not products:
            products = Product.objects.all()
            cache.set(cache_key, products, timeout=60 * 15)
        return products


class AllCategoriesView(ListAPIView):
    serializer_class = CategorySerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        cache_key = 'all_categories'
        categories = cache.get(cache_key)
        if not categories:
            categories = Category.objects.all()
            cache.set(cache_key, categories, timeout=60 * 15)
        return categories


class CategoryProductsView(APIView):
    permission_classes = (AllowAny,)
    def get(self, request, category_slug):
        cache_key = f'category_products_{category_slug}'
        products_data = cache.get(cache_key)

        if not products_data:
            category = get_object_or_404(Category, slug=category_slug)
            products = category.products.all()
            serializer = ProductSerializer(products, many=True, context={'request': request})
            products_data = serializer.data
            cache.set(cache_key, products_data, timeout=60 * 15)

        return Response(products_data, status=status.HTTP_200_OK)


class AddCategoryView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (BasicAuthentication,)

    def perform_create(self, serializer):
        serializer.save()
        cache.delete('all_categories')



class DeleteCategoryView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (BasicAuthentication,)
    def delete(self, request, category_slug):
        category = get_object_or_404(Category, slug=category_slug)
        category.delete()
        cache.delete('all_categories')
        return Response(status=status.HTTP_204_NO_CONTENT)


class EditCategoryView(RetrieveUpdateAPIView):
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (BasicAuthentication,)

    def get_object(self):
        return get_object_or_404(Category, slug=self.kwargs['category_slug'])

    def perform_update(self, serializer):
        serializer.save()
        cache.delete('all_categories')


class ProductDetailView(RetrieveAPIView):
    serializer_class = ProductSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [AllowAny]

    def get_object(self):
        cache_key = f'product_detail_{self.kwargs["product_id"]}'
        product = cache.get(cache_key)
        if not product:
            product = get_object_or_404(Product, id=self.kwargs['product_id'])

            cache.set(cache_key, product, timeout=60 * 15)
        return product


class AttributeKeyView(ListAPIView):
    serializer_class = AttributeKeySerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        cache_key = 'attribute_keys'
        keys = cache.get(cache_key)
        if not keys:
            keys = AttributeKey.objects.all()
            cache.set(cache_key, keys, timeout=60 * 15)
        return keys


class AttributeValueView(ListAPIView):
    serializer_class = AttributeValueSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        cache_key = 'attribute_values'
        values = cache.get(cache_key)
        if not values:
            values = AttributeValue.objects.all()
            cache.set(cache_key, values, timeout=60 * 15)
        return values


class ProductFilterSearchView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category', 'price']
    search_fields = ['slug']


class AddProductView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save()
        cache.delete('all_products')


class DeleteProductView(APIView):
    permission_classes = (IsAuthenticated,)
    def delete(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        product.delete()
        cache.delete('all_products')
        return Response(status=status.HTTP_204_NO_CONTENT)


class EditProductView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProductSerializer

    def get_object(self):
        return get_object_or_404(Product, id=self.kwargs['product_id'])

    def perform_update(self, serializer):
        serializer.save()
        cache.delete('all_products')
