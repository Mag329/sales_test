from django.db import models
from apps.catalog.models import Product

S = 'seafood_demo'
def dbtable(name):
    return f'"{S}"."{name}"'

class Warehouse(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField(unique=True)
    class Meta:
        managed = True
        db_table = dbtable('warehouses')

class Inventory(models.Model):
    pk = models.CompositePrimaryKey('product_id', 'warehouse_id')
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, db_column='product_id', related_name='inventory')
    warehouse = models.ForeignKey(Warehouse, on_delete=models.DO_NOTHING, db_column='warehouse_id', related_name='inventory')
    quantity_t = models.DecimalField(max_digits=12, decimal_places=3)
    reserved_t = models.DecimalField(max_digits=12, decimal_places=3)
    class Meta:
        managed = True
        db_table = dbtable('inventory')

