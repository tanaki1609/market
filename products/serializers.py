from rest_framework import serializers
from .models import Product, Category, Tag, Review


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = 'name'.split()


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = 'id name'.split()


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = 'id text rating created_at'.split()

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    tags = TagSerializer(many=True)
    tags_str = serializers.SerializerMethodField()
    reviews = ReviewSerializer(many=True)

    class Meta:
        model = Product
        fields = 'id reviews name price category tags tags_str tags_str_model category_name'.split()
        depth = 1

    def get_tags_str(self, product):
        l = []
        for tag in product.tags.all():
            l.append(tag.name)
        return l
