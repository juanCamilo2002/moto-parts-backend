from rest_framework import serializers
from .models import Cart, CartItem, Order, OrderItem
from catalog.serializers import ProductSerializer
from catalog.models import Product
from customers.models import Customer
from customers.serializers import CustomerSerializer

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source='product',
        write_only=True
    )

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_id', 'quantity']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, write_only=True)
    items_detail = CartItemSerializer(source='items', many=True, read_only=True)
    customer_id = serializers.PrimaryKeyRelatedField(
        queryset= Customer.objects.all(),
        source='customer',
        write_only=True
    )
    customer = CustomerSerializer(read_only=True)


    class Meta:
        model = Cart
        fields = ['id', 'customer', 'customer_id', 'items', 'items_detail', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at', 'customer']
    
    def create(self, validated_data):
        items_data = validated_data.pop('items', [])
        cart = Cart.objects.create(**validated_data)

        for item_data in items_data:
            CartItem.objects.create(cart=cart, **item_data)
        
        return cart


class OrderItemSerializer(serializers.ModelSerializer):
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source='product',
        write_only=True
    )
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'product_id', 'price']
        read_only_fields = ['id', 'product']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, write_only=True)
    items_detail = OrderItemSerializer(source='items', many=True, read_only=True)
    customer = CustomerSerializer(read_only=True)
    customer_id = serializers.PrimaryKeyRelatedField(
        queryset=Customer.objects.all(),
        source='customer',
        write_only=True
    )

   

    class Meta:
        model = Order
        fields = [
            'id', 'customer', 'seller', 'customer_id', 'total', 'status', 'items', 
            'items_detail', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'customer', 'seller']
    
    def create(self, validated_data):
        items_data = validated_data.pop('items', [])
        order = Order.objects.create(**validated_data)

        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        
        return order

    