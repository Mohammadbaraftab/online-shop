from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from product.models import Product
from category.models import Category
from . import tasks
from django.contrib import messages
from utils import IsUserAdminMixin


class HomeView(View):
    template_name = "home/home.html"
    
    def get(self, request, slug=None):
        categories = Category.objects.filter(is_sub_category = False)
        products = Product.objects.filter(available=True)
        
        if slug:
            category = get_object_or_404(Category, slug=slug)
            products = products.filter(category=category)

        context = {"products": products, "categories": categories}
        return render(request, self.template_name, context)
    

class BucketView(IsUserAdminMixin, View):
    template_name = "home/bucket.html"

    def get(self, request):
        objects = tasks.all_bucket_objects_tasks()
        return render(request, self.template_name, {"objects":objects})
    

class DeleteBucketObjectView(IsUserAdminMixin, View):

    def get(self, request, key):
        tasks.delete_object_task.delay(key)
        messages.success(request, "Your object will be deleted soon", extra_tags="info")
        return redirect("home:bucket")
    

class DownloadBucketObjectView(IsUserAdminMixin, View):

    def get(self, request, key):
        tasks.download_object_task.delay(key)
        messages.success(request, "Your download will be start soon", extra_tags= "info")
        return redirect("home:bucket")
