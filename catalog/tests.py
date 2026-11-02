from django.test import TestCase, Client
from django.urls import reverse
from .models import Category, Product, ProductCharacteristic, Order
from datetime import date, timedelta

class CatalogViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name="Инструмент", slug="instrument")
        self.product = Product.objects.create(
            category=self.category,
            name="Болгарка",
            slug="bolgarka",
            description="Отличная болгарка",
            price_per_day="20.00",
            status="available"
        )
        self.characteristic = ProductCharacteristic.objects.create(
            product=self.product,
            name="Мощность",
            value="1000 Вт"
        )

    def test_product_list_view(self):
        response = self.client.get(reverse('catalog:product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Болгарка")
        self.assertTemplateUsed(response, 'catalog/product_list.html')

    def test_product_list_by_category_view(self):
        response = self.client.get(reverse('catalog:product_list_by_category', args=[self.category.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Болгарка")

    def test_product_detail_view_and_order(self):
        url = reverse('catalog:product_detail', args=[self.product.id, self.product.slug])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Болгарка")
        self.assertContains(response, "Мощность")
        self.assertContains(response, "1000 Вт")

        # Test POST for creating order
        post_data = {
            'customer_name': 'Иван Иванов',
            'customer_phone': '+375291234567',
            'start_date': date.today(),
            'end_date': date.today() + timedelta(days=2),
        }
        response = self.client.post(url, post_data)
        self.assertRedirects(response, url)
        self.assertEqual(Order.objects.count(), 1)

        order = Order.objects.first()
        self.assertEqual(order.customer_name, 'Иван Иванов')
        self.assertEqual(order.product, self.product)
