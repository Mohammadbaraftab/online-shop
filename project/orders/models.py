from django.db import models
from django.contrib.auth import get_user_model
from product.models import Product
from django.core.validators import MaxValueValidator, MinValueValidator


User = get_user_model()

class Order(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="orders")
    is_paid = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    discount = models.PositiveIntegerField(null=True, blank=True, default=None)

    class Meta:
        ordering = ("is_paid", "-updated")

    def __str__(self):
        return f"Order #{self.id} by {self.user.email} ({'Paid' if self.is_paid else 'Unpaid'})"
    
    def get_total_price(self):
        real_price = sum(item.get_cost() for item in self.order_items.all())
        if self.discount:
            discount_value = (self.discount / 100) * real_price
            return int(real_price - discount_value)
        return real_price



class OrderItem(models.Model):
    product = models.ForeignKey(
            to=Product, 
            on_delete=models.CASCADE, 
            related_name="product_order_items"
        )
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE, related_name="order_items")
    quantity = models.PositiveIntegerField(default=0)
    price = models.IntegerField()

    def __str__(self):
        total_price = self.quantity * self.price
        return (
            f"Order #{self.order.id} - {self.quantity} x {self.product.name} "
            f"@ ${self.price} each | Total: ${total_price}"
    )


    def get_cost(self):
        return self.price * self.quantity
    

class Coupan(models.Model):
    code = models.CharField(max_length=20, unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    is_active = models.BooleanField(default=False)
    discount = (models.PositiveSmallIntegerField(validators=
                    [MinValueValidator(0), MaxValueValidator(70)]))
    
    def __str__(self):
        return self.code