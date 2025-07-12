from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from .models import *
from .forms import *
from django.contrib import messages
from django.shortcuts import redirect
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.template import loader
from django.db.models import Q
from django.core.mail import send_mail

def search_products(request):
    query = request.GET.get('q', '')
    results = Product.objects.filter(
        Q(name__icontains=query) | Q(description__icontains=query)
    )
    return render(request, 'styles/search_results.html', {'query': query, 'results': results})


def home(request):
    latest_products = Product.objects.order_by('-id')[:8]
    testimonials = Testimonial.objects.filter(is_approved=True).order_by('-created_at')[:3]
    latest_posts = BlogPost.objects.filter(is_published=True).order_by('-published_at')[:2]
    categories = Category.objects.all()

    return render(request, 'home.html', {
        'latest_products': latest_products,
        'categories': categories,
        'testimonials': testimonials,
        'latest_posts': latest_posts,
    })


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_active=True)
    review_form = ProductReviewForm()
    approved_reviews = product.reviews.filter(is_approved=True).order_by('-created_at')
    return render(request, 'product_detail.html', {'product': product,
    'review_form': review_form,
        'approved_reviews': approved_reviews, 'categories': Category.objects.all()})

def order_product(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_active=True)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.product = product
            order.save()
            send_mail(
                'Nouvelle commande sur Adora Care Style',
                f"Nom : {order.name}\nTéléphone : {order.phone}\nAdresse : {order.address}\nProduit : {product.name}",
                'ntiagda@gmail.com',
                ['ntiagda@gmail.com'],
                fail_silently=True,
            )

            messages.success(request, "Votre commande a été reçue avec succès. Nous vous contacterons bientôt.")
            return redirect('order_success', order_id=order.id)
    else:
        form = OrderForm()

    return render(request, 'styles/order.html', {'form': form, 'product': product, 'categories': Category.objects.all()})

def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'styles/order_success.html', {'order': order})


def generate_facebook_campaign(request):
    products = Product.objects.filter(is_featured=True, is_active=True)
    message = render_to_string('styles/facebook_campaign.txt', {'products': products})
    return HttpResponse(f"<pre>{message}</pre>")


def blog_list(request):
    posts = BlogPost.objects.filter(is_published=True).order_by('-published_at')
    return render(request, 'styles/blog_list.html', {'posts': posts})

def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    return render(request, 'styles/blog_detail.html', {'post': post})


def robots_txt(request):
    template = loader.get_template('robots.txt')
    return HttpResponse(template.render({}, request), content_type="text/plain")

def submit_testimonial(request):
    if request.method == 'POST':
        form = TestimonialForm(request.POST, request.FILES)
        if form.is_valid():
            testimonial = form.save(commit=False)
            testimonial.is_approved = False  # modération
            testimonial.save()
            return render(request, 'styles/testimonial_thankyou.html')
    else:
        form = TestimonialForm()
    return render(request, 'styles/submit_testimonial.html', {'form': form})

def testimonials_list(request):
    testimonials = Testimonial.objects.filter(is_approved=True).order_by('-created_at')
    return render(request, 'styles/testimonials_list.html', {'testimonials': testimonials})

def submit_review(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.is_approved = False  # modération
            review.save()
            return redirect('product_detail', product_id=product.id)
    return redirect('product_detail', pk=product.id)

def products_by_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)
    return render(request, 'styles/category_products.html', {
        'category': category,
        'products': products
    })

def about_page(request):
    return render(request, 'styles/about.html')

def info_line(request):
    return render(request, 'styles/info_line.html')
