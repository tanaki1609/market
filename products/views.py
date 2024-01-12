from collections import OrderedDict

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Product, Category, Tag
from .serializers import ProductSerializer, \
    ProductValidateSerializer, CategorySerializer, TagSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet


class ProductListCreateAPIView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):
        # Step 0. Validate Data
        serializer = ProductValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={'errors': serializer.errors})

        # Step 1. Get data from validated dict
        name = serializer.validated_data.get('name')
        description = serializer.validated_data.get('description')
        price = serializer.validated_data.get('price')
        stock = serializer.validated_data.get('stock')
        is_active = serializer.validated_data.get('is_active')
        category_id = serializer.validated_data.get('category_id')
        tags = serializer.validated_data.get('tags')

        # Step 2. Create Product
        product = Product.objects.create(name=name, description=description, price=price,
                                         stock=stock, is_active=is_active,
                                         category_id=category_id)
        product.tags.set(tags)
        product.save()

        # Step 3. Return created product
        return Response(data={'id': product.id}, status=status.HTTP_201_CREATED)


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = PageNumberPagination
    lookup_field = 'id'



class CustomPagination(PageNumberPagination):
    page_size = 10

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('total', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('data', data)
        ]))


class CategoryListAPIView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = CustomPagination


class CategoryDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'id'


@api_view(['GET', 'PUT', 'DELETE'])
def product_detail_api_view(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(data={'error': 'Product not found'},
                        status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return Response(data=serializer.data)
    elif request.method == 'PUT':
        product.name = request.data.get('name')
        product.price = request.data.get('price')
        product.stock = request.data.get('stock')
        product.description = request.data.get('description')
        product.is_active = request.data.get('is_active')
        product.category_id = request.data.get('category_id')
        product.tags.set(request.data.get('tags'))
        product.save()
        return Response(data={'id': product.id}, status=status.HTTP_201_CREATED)
    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def product_list_api_view(request):
    if request.method == 'GET':
        # Step 1. Collect products from DB
        products = Product.objects.select_related(
            'category'
        ).prefetch_related(
            'tags',
            'reviews'
        ).all()

        # Step 2. Serialize (Reformat) products
        serializer = ProductSerializer(products, many=True)

        # Step 3. Return serialized products
        return Response(data=serializer.data)
    else:
        print(request.user)
        # Step 0. Validate Data
        serializer = ProductValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={'errors': serializer.errors})

        # Step 1. Get data from validated dict
        name = serializer.validated_data.get('name')
        description = serializer.validated_data.get('description')
        price = serializer.validated_data.get('price')
        stock = serializer.validated_data.get('stock')
        is_active = serializer.validated_data.get('is_active')
        category_id = serializer.validated_data.get('category_id')
        tags = serializer.validated_data.get('tags')

        # Step 2. Create Product
        product = Product.objects.create(name=name, description=description, price=price,
                                         stock=stock, is_active=is_active,
                                         category_id=category_id)
        product.tags.set(tags)
        product.save()

        # Step 3. Return created product
        return Response(data={'id': product.id}, status=status.HTTP_201_CREATED)


@api_view(['GET', 'POST'])
def test_api_view(request):
    if request.method == 'GET':
        dict_ = {
            "text": 'hello',
            "int": 100,
            "float": 3.14,
            "bool": True,
            "list": [1, 2, 3],
            "dict": {"a": 1, "b": 2},
        }
        return Response(data=dict_, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        print(request.data)
        return Response()
