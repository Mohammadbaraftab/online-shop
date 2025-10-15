from django.db import models
from category.models import Category  
from django.urls import reverse


class Product(models.Model):
    category = models.ManyToManyField(to=Category, related_name="products")
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    image = models.ImageField()
    price = models.IntegerField()
    description = models.TextField(blank=True)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("product:product_detail", args=[self.slug])
    