# JolNaPu - Multi-Location Stock Inventory Management System

> **JolNaPu** is a web-based Stock & Inventory Management System built with Django. It provides end-to-end tracking for multi-node supply chains, including warehouse depots and retail storefronts, supporting stock intake, inter-location transfers, point-of-sale checkouts, and audit logs.

---

## Table of Contents
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Installation & Setup](#installation--setup)
- [Environment Configuration](#environment-configuration)
- [Database Setup & Seeding](#database-setup--seeding)
- [Default Demo Accounts](#default-demo-accounts)
- [Project Architecture](#project-architecture)
- [Key URL Endpoints](#key-url-endpoints)
- [License](#license)

---

## Features

- **Multi-Location Inventory Tracking**: Manage inventory across multiple nodes (Regional Warehouses and Retail Storefronts).
- **Stock Movement Operations**:
  - **Stock Intake**: Receive incoming product shipments from suppliers into warehouses/stores.
  - **Stock Transfer**: Move items seamlessly between warehouses and retail locations.
  - **Sale Checkout**: Deduct stock upon retail sale with price and quantity calculations.
  - **Manual Adjustments**: Perform manual stock reconciliation and corrections.
- **Audit Logging & History**: Automated logging of all stock adjustments, transfers, sales, and intakes with timestamps and reasons.
- **Low Stock Alerts**: Configurable stock alert thresholds per SKU to prevent stockouts.
- **Role-Based Access Control (RBAC)**: Custom user authentication with 2 roles:
  - **Administrator (`ADMIN`)** — Full system administration, catalog CRUD (Add/Edit/Delete products), and all stock operations.
  - **Inventory Staff (`STAFF`)** — Day-to-day warehouse & retail operations: stock intake, atomic inter-location transfers, point-of-sale checkouts, product catalog viewing, and audit logs.
- **Automated Data Seeding**: Built-in CLI command to populate realistic sample data (users, suppliers, locations, products, and initial stocks).

---

## Tech Stack

- **Backend**: Python, Django
- **Database**: MySQL (via `mysqlclient`) / SQLite
- **Configuration**: `python-decouple` (.env)
- **Frontend**: Django Templates, HTML5, CSS3, JavaScript

---

## Prerequisites

Ensure you have the following installed on your system:

- **Python**: `>= 3.10`
- **Database**: MySQL Server (`>= 8.0` / Laragon / XAMPP) or SQLite3
- **Git**

---

## Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/MonyVisaSU4/stock_inventory_django_final.git
cd stock_inventory_django_final
```

### 2. Create and Activate Virtual Environment
**Windows (PowerShell/CMD):**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## Environment Configuration

Create or update the `.env` file in the root directory:

```env
SECRET_KEY=django-insecure-your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

# MySQL Database Configuration
DB_NAME=stock_inventory_django
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306
```

> **Note**: If using MySQL, create the database before running migrations:
> ```sql
> CREATE DATABASE stock_inventory_django CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
> ```

---

## Database Setup & Seeding

### 1. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 2. Seed Initial Sample Data
Populate the database with demo users, suppliers, locations, and inventory items:
```bash
python manage.py seed_data
```

### 3. Start Development Server
```bash
python manage.py runserver
```
Visit `http://127.0.0.1:8000/` in your browser.

---

## Default Demo Accounts

After running `python manage.py seed_data`, the following test accounts are ready for use:

| Role | Username | Password | Scope |
| :--- | :--- | :--- | :--- |
| **Administrator** | `admin` | `password123` | Full admin, catalog management (Add/Edit/Delete products), stock operations & Django Admin (`/admin/`) |
| **Inventory Staff** | `staff` | `password123` | Stock intake, inter-location transfers, POS retail checkouts, catalog viewing & audit logs |

---

## Project Architecture

```
StockInventory/
├── manage.py                     # Django CLI management utility
├── requirements.txt              # Project dependencies
├── .env                          # Environment variables & DB credentials
├── StockInventory/               # Project configuration
│   ├── settings.py               # Global settings, DB config, installed apps
│   ├── urls.py                   # Root URL router
│   ├── wsgi.py                   # WSGI deployment entry point
│   └── asgi.py                   # ASGI entry point
├── Apps/
│   ├── Auth/                     # Custom User model, RBAC, Authentication views
│   │   ├── models.py             # User (AbstractUser with Role choices)
│   │   ├── views.py              # Login / Logout views
│   │   └── urls.py               # Auth routes
│   └── Inventory/                # Core inventory domain logic
│       ├── models.py             # Supplier, Location, Product, ProductLocation, InventoryLog
│       ├── views.py              # Dashboard, Intake, Transfer, Checkout, Log views
│       ├── services.py           # Inventory business transactions & validations
│       ├── urls.py               # Inventory routing
│       └── management/commands/  # `seed_data` management command
└── Core/                         # Shared UI layout, base templates, and static assets
    ├── templates/                # Base and dashboard HTML templates
    └── static/                   # Stylesheets, scripts, and media
```

---

## Key URL Endpoints

| URL Route | View Name | Description |
| :--- | :--- | :--- |
| `/` | `inventory:dashboard` | Main analytics dashboard & stock KPIs |
| `/products/` | `inventory:product-list` | Product catalog with stock levels across nodes |
| `/intake/` | `inventory:intake` | Receive supplier shipments into locations |
| `/transfer/` | `inventory:transfer` | Inter-node stock transfer (Warehouse $\to$ Store) |
| `/checkout/` | `inventory:checkout` | Retail sale stock deduction |
| `/logs/` | `inventory:logs` | Historical stock movement audit trail |
| `/login/` | `auth:login` | User authentication & sign-in |
| `/admin/` | `admin:index` | Django administrative interface |

---

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## License

Distributed under the MIT License. See `LICENSE` for more information.
