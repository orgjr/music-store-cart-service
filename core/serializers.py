from rest_framework import serializers


class IndexResponseSerializer(serializers.Serializer):
    name = serializers.CharField()
    project_version = serializers.CharField()
    description = serializers.CharField()
    environment = serializers.CharField()
    redoc_url = serializers.CharField()
    health_url = serializers.CharField()
    api_version = serializers.CharField()


class HealthResponseSerializer(serializers.Serializer):
    status = serializers.CharField()
    timestamp = serializers.CharField()
    uptime_seconds = serializers.IntegerField()
