from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.generic.edit import DeleteView, UpdateView

from ecommerce.apps.catalogue.models import Product, ProductImage
from ecommerce.apps.orders.models import Order
from ecommerce.apps.orders.views import user_orders

from .forms import (
    ProductAddForm,
    ProductImageAddForm,
    ProductImageUpdateForm,
    ProductUpdateForm,
    RegistrationForm,
    UserAddressForm,
    UserEditForm,
)
from .models import Address, Customer
from .tokens import account_activation_token


@login_required
def wishlist(request):
    products = Product.objects.filter(users_wishlist=request.user)
    return render(request, "account/dashboard/user_wish_list.html", {"wishlist": products})


@login_required
def add_to_wishlist(request, id):
    product = get_object_or_404(Product, id=id)
    if product.users_wishlist.filter(id=request.user.id).exists():
        # product.users_wishlist.remove(request.user)
        messages.success(request,"宝贝已在心愿清单中了哟")
    else:
        product.users_wishlist.add(request.user)
        messages.success(request, "已添加 " + product.title + " 到你的心愿清单")
    return HttpResponseRedirect(request.META["HTTP_REFERER"])

def remove_from_wishlist(request, id):
    product = get_object_or_404(Product, id=id)
    if product.users_wishlist.filter(id=request.user.id).exists():
        product.users_wishlist.remove(request.user)
        messages.success(request, "已将 " + product.title + " 移出你的心愿清单")
    return HttpResponseRedirect(request.META["HTTP_REFERER"])

@login_required
def dashboard(request):
    orders = user_orders(request)
    return render(request, "account/dashboard/dashboard.html", {"section": "profile", "orders": orders})

@login_required
def finish_confirm(request, order_id):
    if(request.method == "POST") :
        tmp = Order.objects.get(pk = order_id);
        tmp.finish = True;
        tmp.save();
        return redirect("/account/user_orders");
    else :
        return render(request, "account/dashboard/order_finish_confirm.html");

@login_required
def edit_details(request):
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)

        if user_form.is_valid():
            user_form.save()
    else:
        user_form = UserEditForm(instance=request.user)

    return render(request, "account/dashboard/edit_details.html", {"form": user_form})


@login_required
def delete_user(request):
    user = Customer.objects.get(pk=request.user.pk)
    # user.is_active = False
    # user.save()
    logout(request)
    user.delete()
    return redirect("account:delete_confirmation")


def account_register(request):

    if request.user.is_authenticated:
        return redirect("account:dashboard")

    if request.method == "POST":
        registerForm = RegistrationForm(request.POST)
        if registerForm.is_valid():
            user = registerForm.save(commit=False)
            user.email = registerForm.cleaned_data["email"]
            user.set_password(registerForm.cleaned_data["password"])
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = "UESTC跳蚤市场：激活您的账户"
            message = render_to_string(
                "account/registration/account_activation_email.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": account_activation_token.make_token(user),
                },
            )
            user.email_user(subject=subject, message=message)
            return render(request, "account/registration/register_email_confirm.html", {"form": registerForm})
        else:
            return render(request, "account/registration/register.html", {"form": registerForm})
    else:
        registerForm = RegistrationForm()
    return render(request, "account/registration/register.html", {"form": registerForm})


def account_activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Customer.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect("account:dashboard")
    else:
        return render(request, "account/registration/activation_invalid.html")


# Addresses


@login_required
def view_address(request):
    addresses = Address.objects.filter(customer=request.user)
    return render(request, "account/dashboard/addresses.html", {"addresses": addresses})

@login_required
def add_address_tmp(request):
    if request.method == "POST":
        address_form = UserAddressForm(data=request.POST)
        if address_form.is_valid():
            address_form = address_form.save(commit=False)
            address_form.customer = request.user
            address_form.save()
            Address.objects.filter(customer=request.user).update(default=True)
            return HttpResponseRedirect(reverse("checkout:delivery_address"))
        else:
            return HttpResponse("Error handler content", status=400)
    else:
        address_form = UserAddressForm()
    return render(request, "account/dashboard/edit_addresses_tmp.html", {"form": address_form})

@login_required
def add_address(request):
    if request.method == "POST":
        address_form = UserAddressForm(data=request.POST)
        if address_form.is_valid():
            address_form = address_form.save(commit=False)
            address_form.customer = request.user
            address_form.save()
            return HttpResponseRedirect(reverse("account:addresses"))
        else:
            return HttpResponse("Error handler content", status=400)
    else:
        address_form = UserAddressForm()
    return render(request, "account/dashboard/edit_addresses.html", {"form": address_form})


@login_required
def edit_address(request, id):
    if request.method == "POST":
        address = Address.objects.get(pk=id, customer=request.user)
        address_form = UserAddressForm(instance=address, data=request.POST)
        if address_form.is_valid():
            address_form.save()
            return HttpResponseRedirect(reverse("account:addresses"))
    else:
        address = Address.objects.get(pk=id, customer=request.user)
        address_form = UserAddressForm(instance=address)
    return render(request, "account/dashboard/edit_addresses.html", {"form": address_form})


@login_required
def delete_address(request, id):
    address = Address.objects.filter(pk=id, customer=request.user).delete()
    return redirect("account:addresses")


@login_required
def set_default(request, id):
    Address.objects.filter(customer=request.user, default=True).update(default=False)
    Address.objects.filter(pk=id, customer=request.user).update(default=True)

    previous_url = request.META.get("HTTP_REFERER")

    if "delivery_address" in previous_url:
        return redirect("checkout:delivery_address")

    return redirect("account:addresses")


@login_required
def user_orders(request):
    user_id = request.user.id
    orders = Order.objects.filter(user_id=user_id).filter(billing_status=True)
    return render(request, "account/dashboard/user_orders.html", {"orders": orders})

@login_required
def user_product_manage(request):
    user = request.user
    user_products = Product.objects.filter(seller=request.user)
    context = {"user": user, "products": user_products}
    return render(request, "account/dashboard/manage/manage.html", context)

@login_required
def ProductAdd(request):
    if request.method == "POST":
        product_add_form = ProductAddForm(data=request.POST)
        product_image_add_form = ProductImageAddForm(data=request.POST, files=request.FILES)
        if product_add_form.is_valid() and product_image_add_form.is_valid():
            # product是image的外键，要先提交product
            product = product_add_form.save(commit=False)
            # save的表单必须符合数据模型的约束，手动填上必填的字段后再save
            product.seller = request.user
            product.save()
            image = product_image_add_form.save(commit=False)
            image.product = product
            image.save()
            return redirect("account:product_manage")
        else:
            form = {"form": product_add_form, "form_image": product_image_add_form, "update": 0}
            return render(request, "account/dashboard/manage/product_form.html", form)

    elif request.method == "GET":
        product_add_form = ProductAddForm()
        product_image_add_form = ProductImageAddForm()
        form = {"form": product_add_form, "form_image": product_image_add_form, "update": 0}
        return render(request, "account/dashboard/manage/product_form.html", form)
    else:
        return HttpResponse("请使用GET或POST请求数据")


# 使用先删除再添加的方式更新
@login_required
def ProductUpdate(request, pid):
    old_product = Product.objects.get(pk=pid)
    old_images = ProductImage.objects.filter(product=old_product)
    old_image=None
    if len(old_images) : old_image=old_images[0]
    if request.method == "POST":
        product_add_form = ProductUpdateForm(data=request.POST)
        product_image_add_form = ProductImageUpdateForm(data=request.POST, files=request.FILES)
        if product_add_form.is_valid() and product_image_add_form.is_valid():
            old_product.delete()
            # product是image的外键，要先提交product
            product = product_add_form.save(commit=False)
            # save的表单必须符合数据模型的约束，手动填上必填的字段后再save
            product.seller = request.user
            product.save()
            image = product_image_add_form.save(commit=False)
            if(len(request.FILES) == 0) :
                if old_image!=None:
                    image.image = old_image.image
            image.product = product
            image.save()
            return redirect("account:product_manage")
        else:
            form = {"form": product_add_form, "form_image": product_image_add_form, "update": 1}
            return render(request, "account/dashboard/manage/product_form.html", form)
    elif request.method == "GET":
        product_add_form = ProductUpdateForm(initial=dict(old_product.__dict__, **{"category":old_product.category}))
        if(old_image) : product_image_add_form = ProductImageUpdateForm(initial=old_image.__dict__)
        else: product_image_add_form = ProductImageUpdateForm()
        form = {"form": product_add_form, "form_image": product_image_add_form, "update": 1}
        return render(request, "account/dashboard/manage/product_form.html", form)
    else:
        return HttpResponse("请使用GET或POST请求数据")

@login_required
def AllOrder(request):
    products = Product.objects.prefetch_related("order_product").filter(is_active=True).filter(seller=request.user.id)
    print(products)
    return render(request, "account/dashboard/manage/all_order.html", {"products": products})

@login_required
def ItemOrder(request, pid):
    products = Product.objects.prefetch_related("order_product").filter(is_active=True)
    product = get_object_or_404(products, pk=pid, is_active=True)
    return render(request, "account/dashboard/manage/item_order.html", {"product": product})

class ProductDelete(DeleteView):
    model = Product
    success_url = reverse_lazy("account:product_manage")  # 在删除商品后，重定向到我们的商品列表

@login_required
def view_seller(request, seller_id):
    # print(seller_id)
    # sys.stdout.flush()
    seller = Customer.objects.filter(id=seller_id)
    # print(seller)
    # sys.stdout.flush()
    products = Product.objects.prefetch_related("product_image").filter(is_active=True,seller_id=seller_id)
    return render(request, "account/dashboard/view_details.html", {"seller": seller[0], "products": products})
