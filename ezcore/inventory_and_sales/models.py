from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from ezanimal.models import AnimalType, Breed


class InventoryItem(models.Model):
    """
    Model for tracking inventory items such as feed, medicine, equipment, etc.
    """
    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), blank=True)
    
    # Item categorization
    item_type = models.CharField(
        _('item type'),
        max_length=20,
        choices=[
            ('feed', _('Feed')),
            ('medicine', _('Medicine')),
            ('equipment', _('Equipment')),
            ('supplies', _('Supplies')),
            ('other', _('Other'))
        ]
    )
    
    # Inventory tracking
    quantity = models.DecimalField(_('quantity'), max_digits=10, decimal_places=2)
    unit = models.CharField(_('unit'), max_length=50)
    unit_price = models.DecimalField(_('unit price'), max_digits=10, decimal_places=2)
    
    # Stock management
    minimum_stock_level = models.DecimalField(
        _('minimum stock level'),
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_('Minimum quantity before reordering')
    )
    reorder_quantity = models.DecimalField(
        _('reorder quantity'),
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_('Quantity to order when restocking')
    )
    
    # Location
    storage_location = models.CharField(_('storage location'), max_length=255, blank=True)
    
    # Dates
    expiry_date = models.DateField(_('expiry date'), null=True, blank=True)
    
    # Status
    is_active = models.BooleanField(_('active'), default=True)
    
    # Farm owner
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='inventory_items',
        verbose_name=_('owner')
    )
    
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    class Meta:
        verbose_name = _('inventory item')
        verbose_name_plural = _('inventory items')
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} - {self.quantity} {self.unit}"
    
    @property
    def total_value(self):
        """Calculate the total value of the inventory item."""
        return self.quantity * self.unit_price
    
    @property
    def needs_reordering(self):
        """Check if the item needs reordering."""
        if self.minimum_stock_level is not None:
            return self.quantity <= self.minimum_stock_level
        return False


class InventoryTransaction(models.Model):
    """
    Model for tracking inventory transactions (additions, removals, adjustments).
    """
    item = models.ForeignKey(
        InventoryItem,
        on_delete=models.CASCADE,
        related_name='transactions',
        verbose_name=_('item')
    )
    
    # Transaction details
    transaction_date = models.DateField(_('transaction date'))
    transaction_type = models.CharField(
        _('transaction type'),
        max_length=20,
        choices=[
            ('purchase', _('Purchase')),
            ('usage', _('Usage')),
            ('adjustment', _('Adjustment')),
            ('wastage', _('Wastage')),
            ('transfer', _('Transfer')),
            ('other', _('Other'))
        ]
    )
    
    # Quantity and value
    quantity = models.DecimalField(_('quantity'), max_digits=10, decimal_places=2)
    unit_price = models.DecimalField(
        _('unit price'),
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    
    # Reference information
    reference = models.CharField(_('reference'), max_length=255, blank=True)
    supplier = models.CharField(_('supplier'), max_length=255, blank=True)
    
    notes = models.TextField(_('notes'), blank=True)
    recorded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='recorded_inventory_transactions',
        verbose_name=_('recorded by')
    )
    
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    class Meta:
        verbose_name = _('inventory transaction')
        verbose_name_plural = _('inventory transactions')
        ordering = ['-transaction_date', '-created_at']
    
    def __str__(self):
        return f"{self.item.name} - {self.transaction_date} - {self.get_transaction_type_display()}"
    
    def save(self, *args, **kwargs):
        """Update the inventory item quantity when a transaction is saved."""
        is_new = self.pk is None
        
        if is_new:
            # For new transactions, update the inventory item quantity
            if self.transaction_type in ['purchase', 'adjustment', 'transfer']:
                self.item.quantity += self.quantity
            else:  # usage, wastage, etc.
                self.item.quantity -= self.quantity
            
            # Update the unit price if this is a purchase
            if self.transaction_type == 'purchase' and self.unit_price:
                self.item.unit_price = self.unit_price
            
            self.item.save(update_fields=['quantity', 'unit_price', 'updated_at'])
        
        super().save(*args, **kwargs)


class Sale(models.Model):
    """
    Model for tracking sales of animals, milk, or other farm products.
    """
    # Sale details
    sale_date = models.DateField(_('sale date'))
    sale_type = models.CharField(
        _('sale type'),
        max_length=20,
        choices=[
            ('animal', _('Animal')),
            ('milk', _('Milk')),
            ('meat', _('Meat')),
            ('other', _('Other'))
        ]
    )
    
    # Customer information
    customer_name = models.CharField(_('customer name'), max_length=255, blank=True)
    customer_contact = models.CharField(_('customer contact'), max_length=255, blank=True)
    
    # Financial details
    total_amount = models.DecimalField(_('total amount'), max_digits=10, decimal_places=2)
    payment_method = models.CharField(
        _('payment method'),
        max_length=20,
        choices=[
            ('cash', _('Cash')),
            ('bank_transfer', _('Bank Transfer')),
            ('check', _('Check')),
            ('credit', _('Credit')),
            ('other', _('Other'))
        ],
        default='cash'
    )
    payment_status = models.CharField(
        _('payment status'),
        max_length=20,
        choices=[
            ('paid', _('Paid')),
            ('partial', _('Partially Paid')),
            ('pending', _('Pending')),
            ('cancelled', _('Cancelled'))
        ],
        default='paid'
    )
    amount_paid = models.DecimalField(
        _('amount paid'),
        max_digits=10,
        decimal_places=2,
        default=0
    )
    
    # Reference information
    invoice_number = models.CharField(_('invoice number'), max_length=100, blank=True)
    
    notes = models.TextField(_('notes'), blank=True)
    
    # Farm owner
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sales',
        verbose_name=_('owner')
    )
    recorded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='recorded_sales',
        verbose_name=_('recorded by')
    )
    
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    class Meta:
        verbose_name = _('sale')
        verbose_name_plural = _('sales')
        ordering = ['-sale_date', '-created_at']
    
    def __str__(self):
        return f"{self.get_sale_type_display()} - {self.sale_date} - {self.total_amount}"
    
    @property
    def balance_due(self):
        """Calculate the balance due for the sale."""
        return self.total_amount - self.amount_paid


class SaleItem(models.Model):
    """
    Model for individual items in a sale.
    """
    sale = models.ForeignKey(
        Sale,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name=_('sale')
    )
    
    # Item details
    item_type = models.CharField(
        _('item type'),
        max_length=20,
        choices=[
            ('dairy_animal', _('Dairy Animal')),
            ('meat_animal', _('Meat Animal')),
            ('milk', _('Milk')),
            ('meat', _('Meat')),
            ('other', _('Other'))
        ]
    )
    description = models.CharField(_('description'), max_length=255)
    
    # Quantity and price
    quantity = models.DecimalField(_('quantity'), max_digits=10, decimal_places=2)
    unit = models.CharField(_('unit'), max_length=50)
    unit_price = models.DecimalField(_('unit price'), max_digits=10, decimal_places=2)
    
    # Optional references to specific models
    dairy_animal_id = models.IntegerField(_('dairy animal ID'), null=True, blank=True)
    meat_animal_id = models.IntegerField(_('meat animal ID'), null=True, blank=True)
    
    class Meta:
        verbose_name = _('sale item')
        verbose_name_plural = _('sale items')
        ordering = ['sale', 'id']
    
    def __str__(self):
        return f"{self.description} - {self.quantity} {self.unit}"
    
    @property
    def total_price(self):
        """Calculate the total price for the sale item."""
        return self.quantity * self.unit_price


class Expense(models.Model):
    """
    Model for tracking farm expenses.
    """
    # Expense details
    expense_date = models.DateField(_('expense date'))
    expense_type = models.CharField(
        _('expense type'),
        max_length=20,
        choices=[
            ('feed', _('Feed')),
            ('medicine', _('Medicine')),
            ('equipment', _('Equipment')),
            ('utilities', _('Utilities')),
            ('labor', _('Labor')),
            ('maintenance', _('Maintenance')),
            ('veterinary', _('Veterinary')),
            ('transportation', _('Transportation')),
            ('other', _('Other'))
        ]
    )
    
    # Financial details
    amount = models.DecimalField(_('amount'), max_digits=10, decimal_places=2)
    payment_method = models.CharField(
        _('payment method'),
        max_length=20,
        choices=[
            ('cash', _('Cash')),
            ('bank_transfer', _('Bank Transfer')),
            ('check', _('Check')),
            ('credit', _('Credit')),
            ('other', _('Other'))
        ],
        default='cash'
    )
    
    # Vendor information
    vendor = models.CharField(_('vendor'), max_length=255, blank=True)
    
    # Reference information
    receipt_number = models.CharField(_('receipt number'), max_length=100, blank=True)
    
    description = models.TextField(_('description'), blank=True)
    
    # Farm owner
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='expenses',
        verbose_name=_('owner')
    )
    recorded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='recorded_expenses',
        verbose_name=_('recorded by')
    )
    
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    class Meta:
        verbose_name = _('expense')
        verbose_name_plural = _('expenses')
        ordering = ['-expense_date', '-created_at']
    
    def __str__(self):
        return f"{self.get_expense_type_display()} - {self.expense_date} - {self.amount}"
