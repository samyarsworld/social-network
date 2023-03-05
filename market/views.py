from django.shortcuts import render, redirect
from django.urls import reverse
from django.forms import inlineformset_factory

from .filters import OrderFilter
from .models import *
from .forms import OrderForm, CutomerForm, ProductForm


# @admin_only
def home(request):
    customers = Customer.objects.all()
    orders = Order.objects.all().order_by('-customer')
    total_orders = orders.count()
    delivered = Order.objects.filter(status='delivered').count()
    pending = Order.objects.filter(status='pending').count()

    context = {'customers': customers,
            'orders': orders,
            'total_orders': total_orders,
            'delivered': delivered,
            'pending': pending
    }

    return render(request, 'market/home.html', context)


# @admin_only
def products(request):

    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST)
        form.save()
        return redirect(reverse('market:products'))

    context = {
        'products': Product.objects.all(),
        'form': form
    }
    return render(request, 'market/products.html', context)


# @allowed_users(allowed_roles=['admin'])
def customerDetail(request, id):

    customer = Customer.objects.get(id=id)
    #orders = Order.objects.get(customer=id) or:
    orders = customer.has_ordered.all()
    order_count = orders.count()
    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs #queryset


    context = {
        'customer': customer,
        'orders': orders,
        'order_count': order_count,
        'myFilter': myFilter
    }
    return render(request, 'market/customer.html', context)


# @allowed_users(allowed_roles=['customer'])
def createOrder(request, id):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=7 )
    customer = Customer.objects.get(id=id)
    #form = OrderForm(initial={'customer': customer})
    formset = OrderFormSet(queryset=Order.objects.none(),instance=customer)

    if request.method == 'POST':
        #form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance=customer)

        if formset.is_valid():
            formset.customer = id
            formset.save()
            return redirect('home')

    context = {'formset': formset}
    return render(request, 'market/create_order.html', context)


# @allowed_users(allowed_roles=['admin', 'customer'])
def updateOrder(request, id):
    order = Order.objects.get(id=id)
    form = OrderForm(instance=order)

    if request.method == 'POST':
        # By defining instance you actually grab that record from the table rather than creating a new one
        form = OrderForm(request.POST, instance=order)

        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'market/update_order.html', context)



# @allowed_users(allowed_roles=['admin', 'customer'])
def deleteOrder(request, id):
    order = Order.objects.get(id=id)
    if request.method == 'POST':
        order.delete()
        return redirect('home')

    context = {'item': order}
    return render(request, 'market/delete_order.html', context)


# # @allowed_users(allowed_roles=['customer'])
# def settingView(request):
#     form = CutomerForm(instance=request.user.customer)
#     if request.method == 'POST':
#         # you need to capture the post data and the files that are sent, here images
#         form = CutomerForm(request.POST, request.FILES,instance=request.user.customer)

#         if form.is_valid():
#             form.save()
#             return redirect('home')

#     context = {'form': form}
#     return render(request, 'market/account_setting.html', context)

