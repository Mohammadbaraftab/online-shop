from django.db import models
from django.contrib.auth import get_user_model
from product.models import Product

User = get_user_model()

class Order(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="orders")
    is_paid = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("is_paid", "-updated")

    def __str__(self):
        return f"Order #{self.id} by {self.user.username} ({'Paid' if self.is_paid else 'Unpaid'})"
    
    def get_total_price(self):
        return sum(item.get_cost() for item in self.order_items.all())



class OrderItem(models.Model):
    product = models.ForeignKey(
            to=Product, 
            on_delete=models.CASCADE, 
            related_name="product_order_items"
        )
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE, related_name="ordr_items")
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        total_price = self.quantity * self.price
        return (
            f"Order #{self.order.id} - {self.quantity} x {self.product.name} "
            f"@ ${self.price} each | Total: ${total_price}"
    )


    def get_cost(self):
        return self.price * self.quantity