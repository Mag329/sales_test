from django.db import models

from apps.catalog.models import Product
from apps.inventory.models import Warehouse

S = 'seafood_demo'
def dbtable(name):
    return f'"{S}"."{name}"'


class ProductSalesReport(models.Model):
    product_id = models.IntegerField(primary_key=True)
    category_id = models.IntegerField()
    product_name = models.TextField()
    cost_rub_kg = models.DecimalField(max_digits=12, decimal_places=2)
    min_price_rub_kg = models.DecimalField(max_digits=12, decimal_places=2)
    stock_t = models.DecimalField(max_digits=20, decimal_places=3)
    reserved_t = models.DecimalField(max_digits=20, decimal_places=3)
    transit_t = models.DecimalField(max_digits=20, decimal_places=3)
    transit_reserved_t = models.DecimalField(max_digits=20, decimal_places=3)
    week_minus_3_t = models.DecimalField(max_digits=20, decimal_places=3)
    week_minus_2_t = models.DecimalField(max_digits=20, decimal_places=3)
    week_minus_1_t = models.DecimalField(max_digits=20, decimal_places=3)
    week_0_t = models.DecimalField(max_digits=20, decimal_places=3)
    avg_3_weeks_t = models.DecimalField(max_digits=20, decimal_places=3)
    current_month_rub = models.DecimalField(max_digits=24, decimal_places=2)
    class Meta:
        managed = True
        db_table = dbtable('product_sales_report')
