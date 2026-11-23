from django.db import models

S = 'seafood_demo'
def dbtable(name):
    return f'"{S}"."{name}"'

class Category(models.Model):
    id = models.IntegerField(primary_key=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.DO_NOTHING, related_name='children', db_column='parent_id')
    name = models.TextField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    class Meta:
        managed = True
        db_table = dbtable('categories')

class Product(models.Model):
    id = models.IntegerField(primary_key=True)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, db_column='category_id', related_name='products')
    name = models.TextField()
    origin_country = models.TextField()
    package_kg = models.DecimalField(max_digits=6, decimal_places=2)
    cost_rub_kg = models.DecimalField(max_digits=12, decimal_places=2)
    min_price_rub_kg = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    class Meta:
        managed = True
        db_table = dbtable('products')