"""VEDA V2 — Shop API views. Public, no auth required."""
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers, status as drf_status

from .shop_models import ShopCategory, ShopProduct, ShopCartEvent


class ShopProductSerializer(serializers.ModelSerializer):
    category_name    = serializers.CharField(source='category.name', read_only=True)
    category_icon    = serializers.CharField(source='category.icon', read_only=True)
    discount_percent = serializers.ReadOnlyField()
    in_stock         = serializers.ReadOnlyField()

    class Meta:
        model  = ShopProduct
        fields = [
            'id', 'name', 'brand', 'description', 'part_number',
            'price', 'original_price', 'discount_percent',
            'stock', 'in_stock', 'unit', 'image_emoji', 'image_path',
            'compatible_with', 'category_name', 'category_icon',
        ]


class ShopCategorySerializer(serializers.ModelSerializer):
    products = ShopProductSerializer(many=True, read_only=True)

    class Meta:
        model  = ShopCategory
        fields = ['id', 'name', 'slug', 'icon', 'products']


class ShopListView(APIView):
    """GET /api/v1/shop/  — all categories with products"""
    permission_classes = [AllowAny]

    def get(self, request: Request) -> Response:
        component = request.query_params.get('component')
        cats = ShopCategory.objects.prefetch_related('products').all()
        result = []
        for cat in cats:
            prods = cat.products.filter(is_active=True)
            if component:
                prods = prods.filter(compatible_with__icontains=component)
            if prods.exists():
                result.append({
                    'id':       str(cat.id),
                    'name':     cat.name,
                    'slug':     cat.slug,
                    'icon':     cat.icon,
                    'products': ShopProductSerializer(prods, many=True).data,
                })
        return Response(result)


class ShopCartView(APIView):
    """POST /api/v1/shop/cart/  — log add-to-cart (silent)"""
    permission_classes = [AllowAny]

    def post(self, request: Request) -> Response:
        product_id = request.data.get('product_id')
        quantity   = int(request.data.get('quantity', 1))
        session_id = request.data.get('session_id', '')
        try:
            product = ShopProduct.objects.get(id=product_id, is_active=True)
            ShopCartEvent.objects.create(
                product=product, session_id=session_id, quantity=quantity
            )
        except ShopProduct.DoesNotExist:
            pass  # silent
        return Response({'status': 'ok'})
