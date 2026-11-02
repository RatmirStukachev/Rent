from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Category, Product
from .forms import OrderForm

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.all()

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    context = {
        'category': category,
        'categories': categories,
        'products': products
    }
    return render(request, 'catalog/product_list.html', context)


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.product = product
            order.save()
            messages.success(request, 'Ваша заявка на бронирование успешно отправлена!')
            return redirect('catalog:product_detail', id=product.id, slug=product.slug)
    else:
        form = OrderForm()

    context = {
        'product': product,
        'form': form
    }
    return render(request, 'catalog/product_detail.html', context)
