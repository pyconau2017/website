import datetime

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from registrasion.controllers.invoice import InvoiceController
from registrasion.models import Product


class Command(BaseCommand):
    help = "Creates a manual invoice for multiple products against a user."

    def add_arguments(self, parser):
        parser.add_argument('--user', required=True, help='user to add invoice to')
        parser.add_argument('--product', required=True, help='product type of invoice')
        parser.add_argument('--count', required=True, type=int, help='how many products')

    def handle(self, *args, **options):
        product = Product.objects.filter(name=options['product'])[0]

        user = User.objects.filter(username=options['user'])[0]

        due_delta = datetime.timedelta(hours=24)

        description_price_pairs = [(product.name, product.price)] * options['count']

        invoice = InvoiceController.manual_invoice(
            user, due_delta, description_price_pairs
        )

        print(invoice)
