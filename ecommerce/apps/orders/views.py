from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from ecommerce.apps.basket.basket import Basket

from .models import Order


def add(request):
    basket = Basket(request)
    if request.POST.get("action") == "post":

        order_key = request.POST.get("order_key")
        user_id = request.user.id
        baskettotal = basket.get_total_price()

        # Check if order exists
        if Order.objects.filter(order_key=order_key).exists():
            pass
        else:
            for item in basket:
                Order.objects.create(
                    user_id=user_id,
                    full_name="name",
                    address1="add1",
                    address2="add2",
                    total_paid=item["qty"] * item["price"],
                    order_key=order_key,
                    product=item["product"],
                    quantity=item["qty"],
                )
        response = JsonResponse({"success": "Return something"})
        return response

def payment_confirmation(data):
    Order.objects.filter(order_key=data).update(billing_status=True)


def user_orders(request):
    user_id = request.user.id
    orders = Order.objects.filter(user_id=user_id).filter(billing_status=True)
    return orders
