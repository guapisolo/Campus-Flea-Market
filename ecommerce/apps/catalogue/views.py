from django.shortcuts import get_object_or_404, render

from .models import Category, Product
from ecommerce.apps.basket.basket import Basket


def product_all(request):
    if (request.GET.get('search_text') != None) :
        products = Product.objects.prefetch_related("product_image").filter(is_active=True).filter(title__icontains = request.GET['search_text'])
    else : products = Product.objects.prefetch_related("product_image").filter(is_active=True)
    basket = Basket(request)
    return render(request, "catalogue/index.html", {"products": products, "basket": basket})


def category_list(request, category_slug=None):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(
        category__in=Category.objects.get(slug=category_slug).get_descendants(include_self=True)
    )
    basket = Basket(request)
    return render(request, "catalogue/category.html", {"category": category, "products": products, "basket" : basket})


def product_detail(request, pid):
    products = Product.objects.prefetch_related("order_product").filter(is_active=True)
    product = get_object_or_404(products, pk=pid, is_active=True)
    basket = Basket(request)
    return render(request, "catalogue/single.html", {"product": product, "basket": basket})

