from rest_framework import serializers
from .models import Crawling

class CrawlingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crawling
        fields = '__all__'