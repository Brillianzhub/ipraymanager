from collections import defaultdict

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import FeatureClickAggregate
from django.utils.dateparse import parse_datetime
from django.db.models import F


class FeatureClickBulkCreateView(APIView):
    def post(self, request):
        logs = request.data
        if not logs:
            return Response({"message": "No logs received"}, status=400)

        # Step 1: Aggregate counts {(feature, date): total}
        aggregate_counts = {}
        for log in logs:
            feature = log.get("feature")
            ts = parse_datetime(log.get("timestamp"))
            if not feature or not ts:
                continue
            date = ts.date()
            key = (feature, date)
            aggregate_counts[key] = aggregate_counts.get(key, 0) + 1

        # Step 2: Fetch existing aggregates
        features = [k[0] for k in aggregate_counts.keys()]
        dates = [k[1] for k in aggregate_counts.keys()]
        existing_objs = list(FeatureClickAggregate.objects.filter(
            feature__in=features,
            date__in=dates
        ))
        existing_map = {(obj.feature, obj.date): obj for obj in existing_objs}

        # Step 3: Update existing objects
        objs_to_update = []
        for key, count in aggregate_counts.items():
            if key in existing_map:
                obj = existing_map[key]
                obj.count = F('count') + count
                objs_to_update.append(obj)

        if objs_to_update:
            FeatureClickAggregate.objects.bulk_update(
                objs_to_update, ["count"])

        # Step 4: Create new aggregates
        objs_to_create = [
            FeatureClickAggregate(feature=k[0], date=k[1], count=count)
            for k, count in aggregate_counts.items() if k not in existing_map
        ]
        if objs_to_create:
            FeatureClickAggregate.objects.bulk_create(objs_to_create)

        return Response({"message": "Logs aggregated successfully"}, status=201)


class FeatureClickStatsView(APIView):
    def get(self, request):
        period = request.query_params.get("period", "day")  # default is day

        # Map period to date formatting
        # Since aggregates are per day, we can group manually
        if period not in ["day", "week", "month", "year"]:
            return Response({"error": "Invalid period"}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch all aggregates
        raw_data = FeatureClickAggregate.objects.all().order_by("date", "feature")

        # Group data by period and feature
        feature_map = defaultdict(list)
        for row in raw_data:
            # Determine the period label
            if period == "day":
                period_label = row.date
            elif period == "week":
                period_label = row.date.isocalendar()[1]  # week number
            elif period == "month":
                period_label = row.date.month
            elif period == "year":
                period_label = row.date.year

            feature_map[row.feature].append({
                "period": period_label,
                "total": row.count
            })

        # Add trend comparison
        results = []
        for feature, rows in feature_map.items():
            prev_total = None
            for row in rows:
                total = row["total"]
                change = None
                change_percent = None

                if prev_total is not None:
                    change = total - prev_total
                    if prev_total > 0:
                        change_percent = round((change / prev_total) * 100, 2)

                results.append({
                    "period": row["period"],
                    "feature": feature,
                    "total": total,
                    "change": change,
                    "change_percent": change_percent
                })
                prev_total = total

        return Response(results, status=status.HTTP_200_OK)
