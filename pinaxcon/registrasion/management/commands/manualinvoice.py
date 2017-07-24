import datetime

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from registrasion.controllers.invoice import InvoiceController
from registrasion.models import Product


class Command(BaseCommand):
    help = "Creates a manual invoice for multiple products against a user. Can specify multiple products."

    def add_arguments(self, parser):
        parser.add_argument('--user', required=True, help='user to add invoice to')
        parser.add_argument('--product', required=True, action="append", help='product name')
        parser.add_argument('--count', required=True, action="append", type=int, help='how many products')

    def handle(self, *args, **options):
        product_name = options['product']
        count = options['count']

        user = User.objects.filter(username=options['user'])[0]
        due_delta = datetime.timedelta(hours=24)

        if len(product_name) != len(count):
            raise ValueError("The number of products must be equal to the number of product counts.")

        description_price_pairs = []
        for (prod_name, c) in zip(product_name, count):

            product = Product.objects.filter(name=prod_name)[0]

            description_price_pairs += [(product.name, product.price)] * c

        invoice = InvoiceController.manual_invoice(
            user, due_delta, description_price_pairs
        )

        print(invoice)
