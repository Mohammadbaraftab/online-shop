from django.views import View
from django.shortcuts import render, get_object_or_404
from .models import Product
from orders.forms import CartAddForm


class ProductDetailView(View):
    template_name = "home/detail.html"

    def get(self, request, slug):
        product = get_object_or_404(Product, slug = slug)
        form = CartAddForm()

        context = {"product":product, "form":form}
        return render (request, self.template_name, context)
        