from decimal import Decimal
from django.core.management.base import BaseCommand
from Apps.UserManagement.models import User
from Apps.Inventory.models import Category, Product, StockTransaction


class Command(BaseCommand):
    help = 'Seeds sample categories, products (normal, low-stock, and out-of-stock), and audit transactions.'

    def handle(self, *args, **options):
        self.stdout.write("Seeding inventory data...")

        # 1. Admin or staff user for audit records
        admin_user = User.objects.filter(is_superuser=True).first()
        if not admin_user:
            admin_user = User.objects.filter(is_staff=True).first()
        if not admin_user:
            admin_user = User.objects.first()

        # 2. Categories
        electronics, _ = Category.objects.get_or_create(
            name='Electronics',
            defaults={'description': 'Devices, chips, and accessories'}
        )
        hardware, _ = Category.objects.get_or_create(
            name='Hardware & Tools',
            defaults={'description': 'Screws, fasteners, and workshop equipment'}
        )
        office, _ = Category.objects.get_or_create(
            name='Office Supplies',
            defaults={'description': 'Stationery, paper, and desk essentials'}
        )

        # 3. Products
        items = [
            {
                'sku': 'ELEC-1001',
                'name': 'Wireless Barcode Scanner',
                'category': electronics,
                'price': Decimal('79.99'),
                'description': 'Handheld 2.4GHz USB wireless laser barcode scanner.',
                'quantity': 25,
                'low_stock_threshold': 5,
            },
            {
                'sku': 'ELEC-1002',
                'name': 'Thermal Receipt Printer',
                'category': electronics,
                'price': Decimal('149.50'),
                'description': 'High-speed 80mm thermal POS receipt printer.',
                'quantity': 3,  # LOW STOCK
                'low_stock_threshold': 5,
            },
            {
                'sku': 'ELEC-1003',
                'name': 'Industrial Label Maker',
                'category': electronics,
                'price': Decimal('89.00'),
                'description': 'Portable industrial label printer with QWERTY keyboard.',
                'quantity': 0,  # OUT OF STOCK
                'low_stock_threshold': 4,
            },
            {
                'sku': 'HARD-2001',
                'name': 'Heavy Duty Packing Tape Dispenser',
                'category': hardware,
                'price': Decimal('19.99'),
                'description': 'Ergonomic side-loading 2-inch tape gun.',
                'quantity': 42,
                'low_stock_threshold': 10,
            },
            {
                'sku': 'HARD-2002',
                'name': 'Digital Shipping Scale (50kg)',
                'category': hardware,
                'price': Decimal('45.00'),
                'description': 'Stainless steel platform postal weight scale.',
                'quantity': 4,  # LOW STOCK
                'low_stock_threshold': 5,
            },
            {
                'sku': 'OFFC-3001',
                'name': 'Multi-Purpose Copy Paper (500 Sheets)',
                'category': office,
                'price': Decimal('8.50'),
                'description': '20lb letter size 92-bright white printer paper.',
                'quantity': 120,
                'low_stock_threshold': 20,
            },
            {
                'sku': 'OFFC-3002',
                'name': 'Thermal Transfer Ribbon (Wax/Resin)',
                'category': office,
                'price': Decimal('12.00'),
                'description': '110mm x 300m premium barcode ribbon roll.',
                'quantity': 2,  # LOW STOCK
                'low_stock_threshold': 8,
            },
        ]

        for item_data in items:
            product, created = Product.objects.update_or_create(
                sku=item_data['sku'],
                defaults=item_data
            )
            action_verb = "Created" if created else "Updated"
            self.stdout.write(f"  {action_verb} {product.sku} ({product.name}) - Qty: {product.quantity}")

            # Seed an initial stock audit transaction if none exist
            if not product.transactions.exists():
                StockTransaction.objects.create(
                    product=product,
                    user=admin_user,
                    transaction_type=StockTransaction.TransactionType.RESTOCK,
                    quantity_delta=product.quantity,
                    previous_stock=0,
                    new_stock=product.quantity,
                    reason="Initial warehouse stock provisioning"
                )

        self.stdout.write(self.style.SUCCESS("Successfully seeded inventory data!"))
