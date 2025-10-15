from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .cart import Cart
from product.models import Product
from .forms import CartAddForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Order, OrderItem



class CartView(View):
    template_name = "orders/cart.html"

    def get(self, request):
        cart = Cart(request)

        context = {"cart":cart}
        return render(request, self.template_name, context)
    

class CartAddView(View):

    def post(self, request, product_id):
        product = get_object_or_404(Product, id = product_id)
        cart = Cart(request)
        form = CartAddForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            cart.add(product=product, quantity=cleaned_data["quantity"])
        return redirect("orders:cart")
        

class CartRemoveView(View):

    def get(self, request, product_id):
        product = get_object_or_404(Product, id = product_id)
        cart = Cart(request)
        cart.remove(product=product)
        return redirect("orders:cart")


class OrderDetailView(LoginRequiredMixin, View):
    template_name = "orders/order.html"

    def get(self, request, order_id):
        order = get_object_or_404(Order, id = order_id)
        context = {"order":order}
        return render(request, self.template_name, context)


class OrderCreateView(LoginRequiredMixin, View):

    def get(self, request):
        
        cart = Cart(request)
        order = Order.objects.create(user = request.user)
        for item in cart:
            OrderItem.objects.create(
                                    order = order,
                                    product = item["product"],
                                    quantity = item["quantity"],
                                    price = item["price"]
            )
        cart.clear()
        return redirect("orders:order_detail", order.id)