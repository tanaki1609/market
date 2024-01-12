from rest_framework import serializers
from .models import Product, Category, Tag, Review
from rest_framework.exceptions import ValidationError


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = 'id name'.split()


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


class ProductValidateSerializer(serializers.Serializer):
    name = serializers.CharField(required=True, max_length=255, min_length=3)
    description = serializers.CharField(required=False)
    price = serializers.FloatField(min_value=1)
    stock = serializers.IntegerField(max_value=100)
    is_active = serializers.BooleanField()
    category_id = serializers.IntegerField()
    tags = serializers.ListField(child=serializers.IntegerField(min_value=1))

    def validate_category_id(self, category_id):  # 22
        try:
            Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            raise ValidationError('Category does not exist!')
        return category_id

    # def validate_tags(self, tags):  # [1,2,5]
    #     for i in tags:
    #         try:
    #             Tag.objects.get(id=i)
    #         except Tag.DoesNotExist:
    #             raise ValidationError('Tag does not exist!')
    #     return tags
