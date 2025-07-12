from django.contrib import admin, messages
from django.utils.html import format_html
from .models import *
from .utils import generate_flyer
from .facebook_api import post_to_facebook


# -----------------------------------
# 📦 Gestion des catégories
# -----------------------------------
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


# -----------------------------------
# 🖼️ Inline pour les images de produits
# -----------------------------------
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


# -----------------------------------
# 📢 Action personnalisée : campagne Facebook
# -----------------------------------
@admin.action(description="📢 Publier sur Facebook (campagne)")
def launch_facebook_campaign(modeladmin, request, queryset):
    page_id = "634468993092019"
    access_token = "EAAOqNVSOqt4BPLYr7lOGPpMbZCaDuC8dznaQUcPU18RZAdDE4cuNHCscSjkkxWxMS6ZBmZBLPudzAQ03X9t7CLpAICHAIW0uH9WgyhuZAKhgBr0l85xGZC8FfzUKHXQEta41CtAhMhxV4purCaqZBnT2YZB7MCr8GSpZC64aIHRYNCTpIrYfSrU3GYMTFfvJTaHD1d1ZCvKwcvL7wifEGW5GBxu0VB"  # 🔒 À déplacer dans une variable d'environnement !

    for product in queryset:
        message = f"🌟 {product.name}\nPrix : {product.price} FCFA\nCommandez sur WhatsApp 👉 https://wa.me/237690389086?text=Bonjour%20je%20veux%20le%20produit%20{product.name}"
        flyer_path = generate_flyer(product)
        success = post_to_facebook(page_id, access_token, message, flyer_path)

        if success:
            messages.success(request, format_html("✅ <b>{}</b> publié avec succès sur Facebook.", product.name))
        else:
            messages.error(request, format_html("❌ Échec de la publication pour <b>{}</b>.", product.name))


# -----------------------------------
# 🛍️ Gestion des produits
# -----------------------------------
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'stock', 'category', 'is_active', 'is_featured']
    list_filter = ['is_active', 'is_featured', 'category']
    search_fields = ['name', 'description']
    inlines = [ProductImageInline]
    actions = [launch_facebook_campaign]


# -----------------------------------
# 📦 Gestion des commandes
# -----------------------------------
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['product', 'name', 'phone', 'created_at', 'is_processed']
    list_filter = ['is_processed', 'created_at']
    search_fields = ['name', 'phone', 'address', 'product__name']
    readonly_fields = ['created_at']


# -----------------------------------
# 📝 Gestion des articles de blog
# -----------------------------------
@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'published_at', 'is_published']
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title', 'content']
    list_filter = ['is_published', 'published_at']


# -----------------------------------
# 🌟 Gestion des témoignages clients
# -----------------------------------
@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['name', 'rating', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'rating']
    search_fields = ['name', 'message']
    readonly_fields = ['created_at']


# -----------------------------------
# ⭐ Gestion des avis produits
# -----------------------------------
@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'name', 'rating', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'rating']
    search_fields = ['name', 'comment']
    readonly_fields = ['created_at']
