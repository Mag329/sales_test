
from collections import defaultdict
from decimal import Decimal

from apps.catalog.models import Category
from .models import ProductSalesReport


ZERO = Decimal("0")

SUM_FIELDS = (
    "stock_t",
    "reserved_t",
    "in_transit_t",
    "transit_reserved_t",
    "week_minus_3_t",
    "week_minus_2_t",
    "week_minus_1_t",
    "week_current_t",
    "month_revenue_mrub",
)

COLUMNS = [
    {"key": "stock_t", "label": "Общий остаток, т"},
    {"key": "avg_cost_rub_kg", "label": "СС руб/кг"},
    {"key": "reserved_t", "label": "Резерв, т"},
    {"key": "in_transit_t", "label": "В пути, т"},
    {"key": "transit_reserved_t", "label": "Резерв в пути, т"},
    {"key": "min_price_rub_kg", "label": "Мин цена, руб/кг"},
    {"key": "week_minus_3_t", "label": "-3 нед, т"},
    {"key": "week_minus_2_t", "label": "-2 нед, т"},
    {"key": "week_minus_1_t", "label": "-1 нед, т"},
    {"key": "week_current_t", "label": "0 нед, т"},
    {"key": "avg_3_weeks_t", "label": "Ср 3 нед, т"},
    {"key": "month_revenue_mrub", "label": "Тек месяц, Мруб"},
]


def empty_metrics():
    result = {field: ZERO for field in SUM_FIELDS}
    result.update({
        "avg_cost_rub_kg": ZERO,
        "min_price_rub_kg": ZERO,
        "avg_3_weeks_t": ZERO,
    })
    return result


def product_metrics(product):
    return {
        "stock_t": product.stock_t,
        "avg_cost_rub_kg": product.cost_rub_kg,
        "reserved_t": product.reserved_t,
        "in_transit_t": product.transit_t,
        "transit_reserved_t": product.transit_reserved_t,
        "min_price_rub_kg": product.min_price_rub_kg,
        "week_minus_3_t": product.week_minus_3_t,
        "week_minus_2_t": product.week_minus_2_t,
        "week_minus_1_t": product.week_minus_1_t,
        "week_current_t": product.week_0_t,
        "avg_3_weeks_t": product.avg_3_weeks_t,
        "month_revenue_mrub": (
            product.current_month_rub / Decimal("1000000")
        ),
    }


def aggregate_metrics(products):
    products = list(products)
    result = empty_metrics()

    if not products:
        return result

    for product in products:
        metrics = product_metrics(product)

        for field in SUM_FIELDS:
            result[field] += metrics[field]

    # Средневзвешенная себестоимость по остаткам
    total_stock = result["stock_t"]

    if total_stock > 0:
        result["avg_cost_rub_kg"] = (
            sum(
                (
                    product.cost_rub_kg * product.stock_t
                    for product in products
                ),
                ZERO,
            ) / total_stock
        )

    # Минимальная отпускная цена среди товаров
    result["min_price_rub_kg"] = min(
        product.min_price_rub_kg
        for product in products
    )

    result["avg_3_weeks_t"] = (
        result["week_minus_3_t"]
        + result["week_minus_2_t"]
        + result["week_minus_1_t"]
    ) / Decimal("3")

    return result


def serialize_metrics(metrics):
    return {
        key: round(float(value), 3)
        for key, value in metrics.items()
    }


def build_sales_table():
    categories = list(
        Category.objects.all().order_by("name", "id")
    )

    products = list(
        ProductSalesReport.objects.all().order_by(
            "product_name", "product_id"
        )
    )

    categories_by_id = {
        category.id: category
        for category in categories
    }

    children = defaultdict(list)
    products_by_category = defaultdict(list)

    for category in categories:
        parent_id = category.parent_id

        children[parent_id].append(category)

    for product in products:
        products_by_category[product.category_id].append(
            product
        )

    # Все товары
    category_products = {}
    visiting = set()

    def collect_products(category_id):
        if category_id in category_products:
            return category_products[category_id]

        if category_id in visiting:
            raise ValueError("Обнаружен цикл категорий")

        visiting.add(category_id)

        result = list(
            products_by_category.get(category_id, [])
        )

        for child in children.get(category_id, []):
            result.extend(collect_products(child.id))

        visiting.remove(category_id)
        category_products[category_id] = result

        return result

    for category in categories:
        collect_products(category.id)

    rows = []

    def add_category(category, level=0):
        category_id = category.id
        descendants = category_products[category_id]

        direct_products = products_by_category.get(
            category_id, []
        )
        child_categories = children.get(category_id, [])

        rows.append({
            "id": f"category-{category_id}",
            "parent_id": (
                f"category-{category.parent_id}"
                if category.parent_id is not None
                else None
            ),
            "type": "category",
            "level": level,
            "name": category.name,
            "has_children": bool(
                child_categories or direct_products
            ),
            "metrics": serialize_metrics(
                aggregate_metrics(descendants)
            ),
        })

        for child in child_categories:
            add_category(child, level + 1)

        for product in direct_products:
            rows.append({
                "id": f"product-{product.product_id}",
                "parent_id": f"category-{category_id}",
                "type": "product",
                "level": level + 1,
                "name": product.product_name,
                "has_children": False,
                "metrics": serialize_metrics(
                    product_metrics(product)
                ),
            })

    # Корневые категории
    for category in children.get(None, []):
        add_category(category)

    # Товары без категории
    for product in products:
        if product.category_id not in categories_by_id:
            rows.append({
                "id": f"product-{product.product_id}",
                "parent_id": None,
                "type": "product",
                "level": 0,
                "name": product.product_name,
                "has_children": False,
                "metrics": serialize_metrics(
                    product_metrics(product)
                ),
            })

    return {
        "columns": COLUMNS,
        "rows": rows,
        "totals": serialize_metrics(
            aggregate_metrics(products)
        ),
    }
