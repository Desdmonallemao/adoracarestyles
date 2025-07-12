from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/')
    is_main = models.BooleanField(default=False)  # <-- AJOUT

    def __str__(self):
            return f"{self.product.name} - {'PRINCIPALE' if self.is_main else 'secondaire'}"

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_processed = models.BooleanField(default=False)

    def __str__(self):
        return f"Commande de {self.name} - {self.product.name}"

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    image = models.ImageField(upload_to='blog/', blank=True, null=True)
    published_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    message = models.TextField()
    rating = models.PositiveIntegerField(default=5)  # 1 à 5 étoiles
    photo = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.rating}★)"

class ProductReview(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=100)
    rating = models.PositiveIntegerField(choices=[(i, f"{i} étoiles") for i in range(1, 6)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.product.name} - {self.rating}★"

@property
def average_rating(self):
    approved_reviews = self.reviews.filter(is_approved=True)
    if approved_reviews.exists():
        return round(sum([r.rating for r in approved_reviews]) / approved_reviews.count(), 1)
    return 0
