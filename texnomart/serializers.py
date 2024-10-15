from rest_framework import serializers
from .models import Product, Category, AttributeKey, AttributeValue


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']


class AttributeKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeKey
        fields = ['id', 'key']


class AttributeValueSerializer(serializers.ModelSerializer):
    key = serializers.StringRelatedField()

    class Meta:
        model = AttributeValue
        fields = ['id', 'key', 'value']


class ProductSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    attributes = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'images', 'attributes', 'category']

    def get_images(self, obj):
        request = self.context.get('request')
        return [
            request.build_absolute_uri(image.image.url) for image in obj.images.all()
        ]

    def get_attributes(self, obj):
        request = self.context.get('request')
        return [
            {
                "key": AttributeKeySerializer(attribute.key).data,
                "value": attribute.value
            } for attribute in obj.attributes.all()
        ]
