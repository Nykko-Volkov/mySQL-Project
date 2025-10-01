from django import forms
from django.forms import inlineformset_factory
from .models import Order, OrderItem

class OrderForm(forms.ModelForm):
    """Form for creating orders - supports both registered and walk-in customers"""
    
    # Customer type choice - helps decide which fields to show
    customer_type = forms.ChoiceField(
        choices=[
            ('registered', 'Registered Customer'),
            ('walkin', 'Walk-in Customer')
        ],
        widget=forms.RadioSelect,
        initial='walkin',
        label='Customer Type'
    )
    
    class Meta:
        model = Order
        fields = [
            'customer_type',          # New field - registered or walk-in
            'customer',               # Existing registered customer (dropdown)
            'customer_name',          # New field - walk-in customer name
            'customer_phone',         # New field - walk-in customer phone
            'order_type',             # Dine-in, takeaway, delivery
            'table',                  # Which table (if dine-in)
            'status'                  # Order status
        ]
        
        # Make fields look better
        widgets = {
            'customer_name': forms.TextInput(attrs={'placeholder': 'Customer Name'}),
            'customer_phone': forms.TextInput(attrs={'placeholder': 'Phone Number'}),
            'customer': forms.Select(attrs={'class': 'form-control'}),
            'order_type': forms.Select(attrs={'class': 'form-control'}),
            'table': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def clean(self):
        """Make sure either registered customer OR walk-in details are provided"""
        cleaned_data = super().clean()
        customer_type = cleaned_data.get('customer_type')
        customer = cleaned_data.get('customer')
        customer_name = cleaned_data.get('customer_name')
        
        if customer_type == 'registered' and not customer:
            raise forms.ValidationError('Please select a registered customer.')
            
        if customer_type == 'walkin' and not customer_name:
            raise forms.ValidationError('Please enter customer name for walk-in order.')
            
        return cleaned_data

class OrderItemForm(forms.ModelForm):
    """Form for each item in an order (product + quantity)"""
    
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']  # What item and how many
        
        # Make fields look better
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'value': '1'}),
        }

# This creates multiple OrderItem forms within one Order form
# So user can add multiple items (like 2x Burger, 1x Pizza) in one order
OrderItemFormSet = inlineformset_factory(
    parent_model=Order,        # Main form (Order)
    model=OrderItem,           # Sub-forms (OrderItems)
    form=OrderItemForm,        # How each item form looks
    extra=1,                   # Start with 1 empty item form
    can_delete=True            # Allow removing items
)
