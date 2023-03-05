import django_filters
from django_filters import DateFilter, CharFilter
from .models import *

class OrderFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name='date_created', lookup_expr='gte') #gte is greater than and equal to
    end_date = DateFilter(field_name='date_created', lookup_expr='lte') #gte is greater than and equal to
    note = CharFilter(field_name='note', lookup_expr='icontains') # the i at the begining just means igonre sensitivity
    product_name = CharFilter(field_name='product__name', lookup_expr='icontains')
    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['customer', 'date_created', 'product']