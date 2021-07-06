from django.shortcuts import render, redirect
from .models import Order, Product
from django.db.models import Sum


def index(request):
    context = {
        "all_products": Product.objects.all()
    }
    return render(request, "store/index.html", context)


def checkout(request):
    all_quantities = Order.objects.aggregate(Sum('quantity_ordered'))
    total_charge = Order.objects.aggregate(Sum('total_price'))
    total_charge =   total_charge['total_price__sum']
    total_charge = '{0:.2f}'.format(total_charge)
    last_charge = Order.objects.last()
    item_total_charge = last_charge.total_price
    
    context = {
        'item_total_charge': item_total_charge,
        'all_quantities': all_quantities['quantity_ordered__sum'],
        'total_charge': total_charge,
    }

    return render(request, "store/checkout.html", context)   


def process(request):
    print(request.POST)
    quantity_from_form = int(request.POST["quantity"])
    print(int(request.POST["quantity"]))
    this_buy = request.POST["item_id"]
    item_from_form = Product.objects.get(id=this_buy)

    price_from_form = item_from_form.price
    item_total_charge = quantity_from_form * price_from_form
    print("Charging credit card...")
    Order.objects.create(quantity_ordered = quantity_from_form, total_price = item_total_charge)

    return redirect('/checkout')


