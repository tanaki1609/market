from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Product
from .serializers import ProductSerializer


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
        # Step 1. Get data from BODY
        name = request.data.get('name')
        description = request.data.get('description')
        price = request.data.get('price')
        stock = request.data.get('stock')
        is_active = request.data.get('is_active')
        category_id = request.data.get('category_id')
        tags = request.data.get('tags')

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
