from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from .models import DepositProducts, DepositOptions
from .serializers import DepositProductsSerializer, DepositOptionsSerializer
import requests
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model

API_KEY = settings.API_KEY

@api_view(['GET'])
def deposit_products(request):
    deposit_type = request.GET.get('type')
    keyword = request.GET.get('keyword', '')
    if deposit_type == '예금':
        depositproducts = DepositProducts.objects.filter(fin_prdt_nm__contains='예금', kor_co_nm__contains=keyword)
        serializers = DepositProductsSerializer(depositproducts, many=True)
        return Response(serializers.data)
    elif deposit_type == '적금':
        depositproducts = DepositProducts.objects.filter(fin_prdt_nm__contains='적금', kor_co_nm__contains=keyword)
        serializers = DepositProductsSerializer(depositproducts, many=True)
        return Response(serializers.data)

    # else:
    #     return Response({"error": "Invalid type"}, status=status.HTTP_400_BAD_REQUEST)

# 나누지 않고 다 저장
@api_view(['GET'])
def deposit_allproducts(request):
    depositproducts = DepositProducts.objects.all()
    serializer = DepositProductsSerializer(depositproducts, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def deposit_product(request, product_pk):
    if request.method == 'GET':
        deposit_product = DepositProducts.objects.get(pk=product_pk)
        serializers = DepositProductsSerializer(deposit_product)
        return Response(serializers.data)

@api_view(['GET'])
def deposit_product_options(request):
    options = DepositOptions.objects.all()
    serializer = DepositOptionsSerializer(options, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def deposit_products(request):
    deposit_type = request.GET.get('type')
    keyword = request.GET.get('keyword', '')
    if deposit_type == '예금':
        depositproducts = DepositProducts.objects.filter(fin_prdt_nm__contains='예금', kor_co_nm__contains=keyword)
        serializers = DepositProductsSerializer(depositproducts, many=True)
        return Response(serializers.data)
    elif deposit_type == '적금':
        depositproducts = DepositProducts.objects.filter(fin_prdt_nm__contains='적금', kor_co_nm__contains=keyword)
        serializers = DepositProductsSerializer(depositproducts, many=True)
        return Response(serializers.data)

    # else:
    #     return Response({"error": "Invalid type"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def deposit_product(request, product_pk):
    if request.method == 'GET':
        deposit_product = DepositProducts.objects.get(pk=product_pk)
        serializers = DepositProductsSerializer(deposit_product)
        return Response(serializers.data)

@api_view(['GET'])
def deposit_product_options(request):
    options = DepositOptions.objects.all()
    serializer = DepositOptionsSerializer(options, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def fetch_external_deposit_products(request):
    url = "http://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json"
    params = {
        'auth': API_KEY,
        'topFinGrpNo': '020000',
        'pageNo': 1
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        base_list = data.get('result', {}).get('baseList', [])
        for pd in base_list:
            products_data = {
                'fin_prdt_cd': pd.get('fin_prdt_cd'),
                'kor_co_nm': pd.get('kor_co_nm'),
                'fin_prdt_nm': pd.get('fin_prdt_nm'),
                'etc_note': pd.get('etc_note'),
                'join_deny': pd.get('join_deny'),
                'join_member': pd.get('join_member'),
                'join_way': pd.get('join_way'),
                'spcl_cnd': pd.get('spcl_cnd')
            }
            products_serializer = DepositProductsSerializer(data=products_data)
            if products_serializer.is_valid():
                products_serializer.save()

        option_list = data.get('result', {}).get('optionList', [])
        for ol in option_list:
            fin_prdt_cd = ol.get('fin_prdt_cd')
            intr_rate_type_nm = ol.get('intr_rate_type_nm')
            save_trm = ol.get('save_trm')
            if not DepositOptions.objects.filter(fin_prdt_cd=fin_prdt_cd, intr_rate_type_nm=intr_rate_type_nm, save_trm=save_trm).exists():
                product = get_object_or_404(DepositProducts, fin_prdt_cd=fin_prdt_cd)
                option_data = {
                    'product': product.pk,
                    'fin_prdt_cd': fin_prdt_cd,
                    'intr_rate_type_nm': intr_rate_type_nm,
                    'intr_rate': ol.get('intr_rate'),
                    'intr_rate2': ol.get('intr_rate2'),
                    'save_trm': save_trm,
                }
                options_serializer = DepositOptionsSerializer(data=option_data)
                if options_serializer.is_valid():
                    options_serializer.save(product=product)

    url = "http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json"
    params = {
        'auth': API_KEY,
        'topFinGrpNo': '020000',
        'pageNo': 1
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        base_list = data.get('result', {}).get('baseList', [])
        for pd in base_list:
            products_data = {
                'fin_prdt_cd': pd.get('fin_prdt_cd'),
                'kor_co_nm': pd.get('kor_co_nm'),
                'fin_prdt_nm': pd.get('fin_prdt_nm'),
                'etc_note': pd.get('etc_note'),
                'join_deny': pd.get('join_deny'),
                'join_member': pd.get('join_member'),
                'join_way': pd.get('join_way'),
                'spcl_cnd': pd.get('spcl_cnd')
            }
            products_serializer = DepositProductsSerializer(data=products_data)
            if products_serializer.is_valid():
                products_serializer.save()

        option_list = data.get('result', {}).get('optionList', [])
        for ol in option_list:
            fin_prdt_cd = ol.get('fin_prdt_cd')
            intr_rate_type_nm = ol.get('intr_rate_type_nm')
            save_trm = ol.get('save_trm')
            if not DepositOptions.objects.filter(fin_prdt_cd=fin_prdt_cd, intr_rate_type_nm=intr_rate_type_nm, save_trm=save_trm).exists():
                product = get_object_or_404(DepositProducts, fin_prdt_cd=fin_prdt_cd)
                option_data = {
                    'product': product.pk,
                    'fin_prdt_cd': fin_prdt_cd,
                    'intr_rate_type_nm': intr_rate_type_nm,
                    'intr_rate': ol.get('intr_rate'),
                    'intr_rate2': ol.get('intr_rate2'),
                    'save_trm': save_trm,
                }
                options_serializer = DepositOptionsSerializer(data=option_data)
                if options_serializer.is_valid():
                    options_serializer.save(product=product)
    return Response({"message": "Data fetched successfully"}, status=status.HTTP_200_OK)

User = get_user_model()

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def join_product(request):
    product_id = request.data.get('productId')
    try:
        product = DepositProducts.objects.get(id=product_id)
        user = request.user
        user.joinedProducts.add(product)
        user.save()
        return Response({'status': 'success'}, status=200)
    except DepositProducts.DoesNotExist:
        return Response({'status': 'Product not found'}, status=404)
    except Exception as e:
        return Response({'status': 'error', 'message': str(e)}, status=500)
    

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_join_product(request, product_id):
    try:
        print(f"product_id: {product_id}")
        product = DepositProducts.objects.get(id=product_id) # 수정된 부분
        user = request.user
        user.joinedProducts.remove(product)
        user.save()
        return Response({'status': 'success'}, status=200)
    except DepositProducts.DoesNotExist:
        return Response({'status': 'Product not found'}, status=404)
    except Exception as e:
        return Response({'status': 'error', 'message': str(e)}, status=500)