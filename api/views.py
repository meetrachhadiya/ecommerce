import json
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import viewsets
from rest_framework.response import Response

from products.models import Product

from api.serializers import ProductSerializer, LoginSerializer


@api_view(['POST'])
def login(request):
    data = request.data
    serializer = LoginSerializer(data=data)

    if serializer.is_valid(raise_exception=True):
        print(serializer.data)
        return Response({
            "status" : 200,
            "message" : "success",
            "data" : serializer.data,
        })


@api_view(['GET', 'POST', 'PATCH', 'DELETE'])
def products(request, *args, **kwargs):
    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response({
            "status" : 200,
            "message" : "success",
            "data" : serializer.data,
        })

        # data = {}
        # try:
        #     data = json.loads(request.body)
        # except Exception as e:
        #       print(e)

        # print(request.body)
        # print(data)
        # print(request.GET)

        # return JsonResponse(data)

    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status" : 200,
                "message" : "success",
                "data" : serializer.data,
            })
        return Response({
            "status" : 400,
            "message" : "error",
            "data" : serializer.errors,
        }, status=400)
    
    elif request.method == 'PATCH':
        data = request.data
        product = Product.objects.get(uid = data['uid'])
        serializer = ProductSerializer(instance=product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status" : 200,
                "message" : "success",
                "data" : serializer.data,
            })
        return Response({
            "status" : 400,
            "message" : "error",
            "data" : serializer.errors,
        }, status=400)
    
    elif request.method == 'DELETE':
        data = request.data
        product = Product.objects.get(uid = data['uid'])
        product.delete()
        return Response({
            "status" : 200,
            "message" : "Data Deleted Successfully",
        })
    
    
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer