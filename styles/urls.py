from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('produit/<int:product_id>/', views.product_detail, name='product_detail'),
    path('produit/<int:product_id>/commande/', views.order_product, name='order_product'),
    path('campagne-facebook/', views.generate_facebook_campaign, name='facebook_campaign'),
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path("robots.txt", views.robots_txt, name="robots_txt"),
    path('avis/', views.testimonials_list, name='testimonials_list'),
    path('laisser-un-avis/', views.submit_testimonial, name='submit_testimonial'),
    path('product/<int:product_id>/review/', views.submit_review, name='submit_review'),
    path('recherche/', views.search_products, name='search_products'),
    path('categorie/<slug:slug>/', views.products_by_category, name='products_by_category'),
    path('a-propos/', views.about_page, name='about'),
    path('info-line/', views.info_line, name='info_line'),
    path('commande/succes/<int:order_id>/', views.order_success, name='order_success'),

]
