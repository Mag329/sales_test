
from rest_framework import serializers


class SalesMetricsSerializer(serializers.Serializer):
    stock_t = serializers.FloatField()
    avg_cost_rub_kg = serializers.FloatField()
    reserved_t = serializers.FloatField()
    in_transit_t = serializers.FloatField()
    transit_reserved_t = serializers.FloatField()
    min_price_rub_kg = serializers.FloatField()

    week_minus_3_t = serializers.FloatField()
    week_minus_2_t = serializers.FloatField()
    week_minus_1_t = serializers.FloatField()
    week_current_t = serializers.FloatField()

    avg_3_weeks_t = serializers.FloatField()
    month_revenue_mrub = serializers.FloatField()


class SalesTableRowSerializer(serializers.Serializer):
    id = serializers.CharField()
    parent_id = serializers.CharField(
        allow_null=True,
    )
    type = serializers.ChoiceField(
        choices=["category", "product"],
    )
    level = serializers.IntegerField()
    name = serializers.CharField()
    has_children = serializers.BooleanField()

    metrics = SalesMetricsSerializer()


class SalesTableResponseSerializer(serializers.Serializer):
    columns = serializers.ListField(
        child=serializers.DictField(),
    )
    rows = SalesTableRowSerializer(many=True)
    totals = SalesMetricsSerializer()
