from rest_framework import serializers
from .models import Image

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'original', 'processed', 'width', 'height', 'shape', 'uploaded_at']
        read_only_fields = ['processed', 'uploaded_at']
