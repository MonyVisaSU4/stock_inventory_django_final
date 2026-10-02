from django.core.management.base import BaseCommand
from Apps.Auth.models import User
from Apps.Inventory.models import Supplier, Location, Product, ProductLocation, InventoryLog


class Command(BaseCommand):
    help = 'Seeds initial users, suppliers, multi-location nodes, products, and inventory stock'

    def handle(self, *args, **options):
        self.stdout.write("Starting database seed...")

        # 1. Users (2 Roles: Administrator & Inventory Staff)
        users_data = [
            {'username': 'admin', 'email': 'admin@invenstock.com', 'role': 'ADMIN', 'is_staff': True, 'is_superuser': True},
            {'username': 'staff', 'email': 'staff@invenstock.com', 'role': 'STAFF', 'is_staff': False, 'is_superuser': False},
        ]

        for u in users_data:
            user, created = User.objects.get_or_create(
                username=u['username'],
                defaults={
                    'email': u['email'],
                    'role': u['role'],
                    'status': 'ACTIVE',
                    'is_staff': u['is_staff'],
                    'is_superuser': u['is_superuser'],
                }
            )
            user.set_password('password123')
            user.role = u['role']
            user.status = 'ACTIVE'
            user.is_staff = u['is_staff']
            user.is_superuser = u['is_superuser']
            user.save()
            action = "Created" if created else "Updated"
            self.stdout.write(f" - {action} user: {user.username} ({user.role}) [Password: password123]")

        # Clean up obsolete legacy users if present
        User.objects.filter(username__in=['manager', 'cashier']).delete()

        # 2. Suppliers
        suppliers_data = [
            {'name': 'Apex Logistics & Tech', 'contact_email': 'contact@apexlogistics.io', 'contact_phone': '+1 (555) 234-5678'},
            {'name': 'Nordic Components Corp', 'contact_email': 'supply@nordiccorp.eu', 'contact_phone': '+44 20 7946 0912'},
            {'name': 'Pacific Rim Electronics', 'contact_email': 'orders@pacificrimelec.com', 'contact_phone': '+81 3 5555 0143'},
        ]
        suppliers = []
        for s in suppliers_data:
            supp, _ = Supplier.objects.get_or_create(name=s['name'], defaults=s)
            suppliers.append(supp)

        # 3. Locations
        locations_data = [
            {'name': 'Central Regional Hub (WH-01)', 'location_type': 'WAREHOUSE'},
            {'name': 'North Distribution Depot (WH-02)', 'location_type': 'WAREHOUSE'},
            {'name': 'Downtown Flagship Store (ST-01)', 'location_type': 'STORE'},
            {'name': 'Westfield Mall Store (ST-02)', 'location_type': 'STORE'},
        ]
        locations = []
        for loc_data in locations_data:
            loc, _ = Location.objects.get_or_create(name=loc_data['name'], defaults=loc_data)
            locations.append(loc)

        wh_main = locations[0]
        wh_north = locations[1]
        store_downtown = locations[2]
        store_mall = locations[3]

        # 4. Products & Stocks
        products_data = [
            {
                'sku': 'SKU-LAP-001',
                'name': 'Titan Ultra Pro Laptop 16"',
                'description': 'High-performance workstation laptop with 32GB RAM & 1TB NVMe SSD',
                'retail_price': 1899.00,
                'cost_price': 1250.00,
                'supplier': suppliers[0],
                'low_stock_alert': 5,
                'stocks': {wh_main: 45, wh_north: 20, store_downtown: 6, store_mall: 4}
            },
            {
                'sku': 'SKU-MON-002',
                'name': 'Curved 34" Gaming Monitor 165Hz',
                'description': 'Ultrawide Quad HD HDR Display with USB-C Hub',
                'retail_price': 499.99,
                'cost_price': 320.00,
                'supplier': suppliers[1],
                'low_stock_alert': 8,
                'stocks': {wh_main: 30, wh_north: 15, store_downtown: 8, store_mall: 2}
            },
            {
                'sku': 'SKU-KBD-003',
                'name': 'Mechanical RGB Wireless Keyboard',
                'description': 'Hot-swappable tactile switches with aluminum chassis',
                'retail_price': 129.50,
                'cost_price': 65.00,
                'supplier': suppliers[2],
                'low_stock_alert': 10,
                'stocks': {wh_main: 120, wh_north: 60, store_downtown: 25, store_mall: 18}
            },
            {
                'sku': 'SKU-MOU-004',
                'name': 'Precision Ergonomic Mouse',
                'description': 'Dual-mode Bluetooth/2.4G optical sensor 26K DPI',
                'retail_price': 79.99,
                'cost_price': 38.00,
                'supplier': suppliers[2],
                'low_stock_alert': 15,
                'stocks': {wh_main: 80, wh_north: 40, store_downtown: 14, store_mall: 3}
            },
            {
                'sku': 'SKU-HDP-005',
                'name': 'Studio ANC Wireless Headphones',
                'description': 'Active noise-canceling over-ear headphones with 40h battery',
                'retail_price': 249.00,
                'cost_price': 140.00,
                'supplier': suppliers[0],
                'low_stock_alert': 6,
                'stocks': {wh_main: 15, wh_north: 10, store_downtown: 3, store_mall: 1}
            },
        ]

        for p_data in products_data:
            stocks_map = p_data.pop('stocks')
            product, created = Product.objects.get_or_create(sku=p_data['sku'], defaults=p_data)
            
            for loc, qty in stocks_map.items():
                pl, _ = ProductLocation.objects.get_or_create(
                    product=product,
                    location=loc,
                    defaults={'quantity': qty}
                )
                pl.quantity = qty
                pl.save()

            # Record initial intake log
            InventoryLog.objects.get_or_create(
                product=product,
                log_type='STOCK_IN',
                quantity_changed=product.total_stock,
                destination_location=wh_main,
                defaults={'reason': 'Initial warehouse seeding inventory'}
            )
            self.stdout.write(f" - Seeded Product: {product.sku} ({product.name}) with {product.total_stock} units across nodes.")

        self.stdout.write(self.style.SUCCESS("✓ Successfully seeded database with sample data!"))
