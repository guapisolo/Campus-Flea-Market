import decimal
import json
import sys

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render
from ecommerce.apps.account.models import Address
from ecommerce.apps.basket.basket import Basket
from ecommerce.apps.catalogue.models import Product
from ecommerce.apps.orders.models import Order
from ecommerce.apps.account.models import Customer

from .models import DeliveryOptions


@login_required
def deliverychoices(request):
    deliveryoptions = DeliveryOptions.objects.filter(is_active=True)
    basket = Basket(request)
    return render(request, "checkout/delivery_choices.html", {"deliveryoptions": deliveryoptions, "basket": basket})


def testdb(request):
    d = DeliveryOptions.objects.all();
    d.delete();
    if request.method == "GET":
        tmp = DeliveryOptions(
            delivery_name="京东",
            delivery_method="飞机",
            delivery_price=0.0,
            delivery_timeframe="20221115",
            delivery_window="不知道",
            order="0",
        )
        tmp.save()
        tmp = DeliveryOptions(
            delivery_name="淘宝",
            delivery_method="火车",
            delivery_price=0.0,
            delivery_timeframe="20221101",
            delivery_window="不知道",
            order="0",
        )
        tmp.save()
        return HttpResponse("ok")
    else:
        return HttpResponse("wrong")


@login_required
def basket_update_delivery(request):
    basket = Basket(request)
    if request.POST.get("action") == "post":
        delivery_option = int(request.POST.get("deliveryoption"))
        delivery_type = DeliveryOptions.objects.get(id=delivery_option)
        updated_total_price = basket.basket_update_delivery(delivery_type.delivery_price)

        session = request.session
        if "purchase" not in request.session:
            session["purchase"] = {
                "delivery_id": delivery_type.id,
            }
        else:
            session["purchase"]["delivery_id"] = delivery_type.id
            session.modified = True

        # print("getsubtotal", basket.get_subtotal_price())
        # sys.stdout.flush()

        response = JsonResponse(
            {
                "total": updated_total_price,
                "delivery_price": delivery_type.delivery_price,
                "sub_total": basket.get_subtotal_price(),
            }
        )
        return response


@login_required
def delivery_address(request):

    session = request.session
    if "purchase" not in request.session:
        messages.success(request, "Please select delivery option")
        return HttpResponseRedirect(request.META["HTTP_REFERER"])

    addresses = Address.objects.filter(customer=request.user).order_by("-default")
    deliveryoptions = DeliveryOptions.objects.filter(is_active=True)
    basket = Basket(request)

    # print(addresses)
    # sys.stdout.flush()

    if addresses.count() == 0:
        return render(
            request,
            "checkout/delivery_address.html",
            {"addresses": addresses, "deliveryoptions": deliveryoptions, "basket": basket},
        )
    elif "address" not in request.session:
        session["address"] = {"address_id": str(addresses[0].id)}
        # print("-1")
        # sys.stdout.flush()
    else:
        session["address"]["address_id"] = str(addresses[0].id)
        session.modified = True

    return render(
        request,
        "checkout/delivery_address.html",
        {"addresses": addresses, "deliveryoptions": deliveryoptions, "basket": basket},
    )


@login_required
def payment_selection(request):

    session = request.session
    if "address" not in request.session:
        messages.success(request, "Please select address option")
        return HttpResponseRedirect(request.META["HTTP_REFERER"])

    deliveryoptions = DeliveryOptions.objects.filter(is_active=True)
    basket = Basket(request)

    return render(request, "checkout/payment_selection.html", {"basket": basket})


####
# PayPay
####
from paypalcheckoutsdk.orders import OrdersGetRequest

from .paypal import PayPalClient


@login_required
def payment_complete(request):

    print(request)
    sys.stdout.flush()

    if request.method == "GET":
        user_id = request.user.id

        customer = Customer(request)
        addresses = Address.objects.filter(customer=request.user, default=True)
        address = addresses[0]
        basket = Basket(request)

        # print(customer, address.address_line, address.address_line2)
        # sys.stdout.flush()
        # total = basket.get_total_price()
        # print(total)
        # sys.stdout.flush()
        sg = 1
        for item in basket:
            if(item["qty"] > item["product"].quantity) :
                sg = 0
                break
        if(sg != 1) :
            return HttpResponse("有的商品已经卖光了")
        for item in basket:
            tmp = item["product"]
            tmp.quantity = tmp.quantity - item["qty"]
            tmp.save()

        for item in basket:
            order = Order.objects.create(
                user_id=user_id,
                full_name=address.full_name,
                email=customer.email,
                address1=address.address_line,
                address2=address.address_line2,
                postal_code=address.postcode,
                city=address.town_city,
                phone=address.phone,
                country_code=114514,
                total_paid=item["qty"] * item["price"],
                order_key=0,
                payment_option="paypal",
                billing_status=True,
                product=item["product"],
                quantity=item["qty"],
            )

        basket.clear()
        return render(request, "checkout/payment_successful.html", {})
        # return render(request, "checkout/payment_successful.html", {"account": customer})
    else:
        return HttpResponse("wrong")


# @login_required
# def payment_complete(request):
#     PPClient = PayPalClient()

#     body = json.loads(request.body)
#     data = body["orderID"]
#     user_id = request.user.id

#     requestorder = OrdersGetRequest(data)
#     response = PPClient.client.execute(requestorder)

#     total_paid = response.result.purchase_units[0].amount.value

#     basket = Basket(request)
#     order = Order.objects.create(
#         user_id=user_id,
#         full_name=response.result.purchase_units[0].shipping.name.full_name,
#         email=response.result.payer.email_address,
#         address1=response.result.purchase_units[0].shipping.address.address_line_1,
#         address2=response.result.purchase_units[0].shipping.address.admin_area_2,
#         postal_code=response.result.purchase_units[0].shipping.address.postal_code,
#         country_code=response.result.purchase_units[0].shipping.address.country_code,
#         total_paid=response.result.purchase_units[0].amount.value,
#         order_key=response.result.id,
#         payment_option="paypal",
#         billing_status=True,
#     )
#     order_id = order.pk

#     for item in basket:
#         OrderItem.objects.create(order_id=order_id, product=item["product"], price=item["price"], quantity=item["qty"])

#     return JsonResponse("Payment completed!", safe=False)


# @login_required
# def payment_successful(request):
#     basket = Basket(request)
#     basket.clear()
#     return render(request, "checkout/payment_successful.html", {})
