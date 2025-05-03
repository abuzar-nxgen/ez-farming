from rest_framework import serializers
from ezcore.inventory_and_sales.models import (
    InventoryItem, InventoryTransaction, Sale, SaleItem, Expense
)


class InventoryItemSerializer(serializers.ModelSerializer):
    """Serializer for the InventoryItem model."""
    item_type_display = serializers.ReadOnlyField(source='get_item_type_display')
    total_value = serializers.ReadOnlyField()
    needs_reordering = serializers.ReadOnlyField()
    
    class Meta:
        model = InventoryItem
        fields = [
            'id', 'name', 'description', 'item_type', 'item_type_display',
            'quantity', 'unit', 'unit_price', 'total_value',
            'minimum_stock_level', 'reorder_quantity', 'needs_reordering',
            'storage_location', 'expiry_date', 'is_active', 'owner',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class InventoryTransactionSerializer(serializers.ModelSerializer):
    """Serializer for the InventoryTransaction model."""
    item_name = serializers.ReadOnlyField(source='item.name')
    transaction_type_display = serializers.ReadOnlyField(source='get_transaction_type_display')
    
    class Meta:
        model = InventoryTransaction
        fields = [
            'id', 'item', 'item_name', 'transaction_date', 'transaction_type',
            'transaction_type_display', 'quantity', 'unit_price',
            'reference', 'supplier', 'notes', 'recorded_by',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class SaleItemSerializer(serializers.ModelSerializer):
    """Serializer for the SaleItem model."""
    item_type_display = serializers.ReadOnlyField(source='get_item_type_display')
    total_price = serializers.ReadOnlyField()
    
    class Meta:
        model = SaleItem
        fields = [
            'id', 'sale', 'item_type', 'item_type_display', 'description',
            'quantity', 'unit', 'unit_price', 'total_price',
            'dairy_animal_id', 'meat_animal_id'
        ]
        read_only_fields = ['id']


class SaleSerializer(serializers.ModelSerializer):
    """Serializer for the Sale model."""
    items = SaleItemSerializer(many=True, read_only=True)
    sale_type_display = serializers.ReadOnlyField(source='get_sale_type_display')
    payment_method_display = serializers.ReadOnlyField(source='get_payment_method_display')
    payment_status_display = serializers.ReadOnlyField(source='get_payment_status_display')
    balance_due = serializers.ReadOnlyField()
    
    class Meta:
        model = Sale
        fields = [
            'id', 'sale_date', 'sale_type', 'sale_type_display',
            'customer_name', 'customer_contact',
            'total_amount', 'payment_method', 'payment_method_display',
            'payment_status', 'payment_status_display', 'amount_paid', 'balance_due',
            'invoice_number', 'notes', 'owner', 'recorded_by',
            'created_at', 'updated_at', 'items'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ExpenseSerializer(serializers.ModelSerializer):
    """Serializer for the Expense model."""
    expense_type_display = serializers.ReadOnlyField(source='get_expense_type_display')
    payment_method_display = serializers.ReadOnlyField(source='get_payment_method_display')
    
    class Meta:
        model = Expense
        fields = [
            'id', 'expense_date', 'expense_type', 'expense_type_display',
            'amount', 'payment_method', 'payment_method_display',
            'vendor', 'receipt_number', 'description',
            'owner', 'recorded_by', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
