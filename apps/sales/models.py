from django.db import models

from apps.catalog.models import Product
from apps.inventory.models import Warehouse

S = 'seafood_demo'
def dbtable(name):
    return f'"{S}"."{name}"'


class Sale(models.Model):
    id = models.IntegerField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, db_column='product_id', related_name='sales')
    warehouse = models.ForeignKey(Warehouse, on_delete=models.DO_NOTHING, db_column='warehouse_id', related_name='sales')
    sold_on = models.DateField()
    quantity_t = models.DecimalField(max_digits=12, decimal_places=3)
    price_rub_kg = models.DecimalField(max_digits=12, decimal_places=2)
    class Meta:
        managed = True
        db_table = dbtable('sales')
