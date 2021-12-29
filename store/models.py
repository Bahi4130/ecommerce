from django.db import models
from django.urls import reverse

from category.models import Category


class Product(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(max_length=500, blank=True)
    price = models.IntegerField()
    image = models.ImageField(upload_to='photos/products')
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])

    def __str__(self):
        return self.product_name


class VariationManager(models.Manager):  # ToDo: Use Queryset instead of Manager
    def colors(self):
        return super(VariationManager, self).filter(variation_category='color')

    def sizes(self):
        return super(VariationManager, self).filter(variation_category='size')


variation_category_choice = (  # ToDo: Move it to Variation model scope and create constants for choice tuples. (Use IntegerField instead of CharField?)
    ('color', 'color'),
    ('size', 'size'),
)


class Variation(models.Model):
    objects = VariationManager()

    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # ToDo: Set related_name attr. and update product_detail.html
    variation_category = models.CharField(max_length=100, choices=variation_category_choice)
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.variation_value
