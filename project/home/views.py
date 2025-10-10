from django.shortcuts import render
from django.views import View
from product.models import Product


class HomeView(View):
    def get(self, request):
        products = Product.objects.filter(available = True)
        return render(request, "home/home.html", {"products":products})
    

class HomeBucketView(View):
    template_name = "home/bucket.html"

    def get(self, request):
        return render(request, self.template_name)
