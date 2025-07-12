from django import forms
from .models import *

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['name', 'phone', 'address', 'note']
        widgets = {
            'note': forms.Textarea(attrs={'rows': 3}),
        }


class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ['name', 'message', 'rating', 'photo']


class ProductReviewForm(forms.ModelForm):
    class Meta:
        model = ProductReview
        fields = ['name', 'rating', 'comment']
