def site_context(request):
    """Global context available to every template."""
    return {
        'SITE_NAME': 'Stock Inventory Management System',
    }
