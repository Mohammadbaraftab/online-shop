from django.views import View
from django.shortcuts import render, get_object_or_404
from .models import Product


class ProductDetailView(View):

    def get(self, request, slug):
        product = get_object_or_404(Product, slug = slug)
        return render (request, "home/detail.html", {"product":product})
        