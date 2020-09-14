from rest_framework import serializers
from store.models import (
    Item,
    ItemVariant,
    Category,
    SubCategory,
    SubCategoryClass,
    Collection,
    Specification,
    Image,
    Offer
)


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = [
            'image_xlarge',
            'image_large',
            'image_nslarge',
            'image_normal',
            'image_medium',
            'image_small',
            'image_xsmall'
        ]


class SpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specification
        fields = [
            'shoe_size',
            'clothing_size',
        ]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'name',
            'slug',
            'description'
        ]


class SubCategorySerializer(serializers.ModelSerializer):
    category = CategorySerializer(required=False, read_only=True)

    class Meta:
        model = SubCategory
        fields = [
            'name',
            'slug',
            'description',
            'created_date',
            'featured',
            'category'
        ]


class MiniSubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = [
            'name',
            'slug',
            'featured'
        ]


class SubCategoryClassSerializer(serializers.ModelSerializer):
    subcategory = MiniSubCategorySerializer(required=False, read_only=True)
    category = CategorySerializer(required=False, read_only=True)

    class Meta:
        model = SubCategoryClass
        fields = [
            'name',
            'slug',
            'description',
            'created_date',
            'featured',
            'subcategory',
            'category'
        ]


class MiniSubCategoryClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategoryClass
        fields = [
            'name',
            'slug',
            'featured'
        ]


class ItemVariantSerializer(serializers.ModelSerializer):
    specifications = SpecificationSerializer(
        required=False, read_only=True, many=True)
    images = ImageSerializer(required=False, read_only=True, many=True)

    class Meta:
        model = ItemVariant
        fields = [
            'name',
            'in_stock',
            'images',
            'specifications'
        ]


class ItemSerializer(serializers.ModelSerializer):
    subcategory_classes = MiniSubCategoryClassSerializer(
        required=False, read_only=True, many=True)
    subcategories = MiniSubCategorySerializer(
        required=False, read_only=True, many=True)
    categories = CategorySerializer(required=False, read_only=True, many=True)
    variants = ItemVariantSerializer(required=False, read_only=True, many=True)

    class Meta:
        model = Item
        fields = [
            'id',
            'name',
            'description',
            'price',
            'discount_price',
            'discount',
            'variants',
            'created_date',
            'badge',
            'video',
            'subcategory_classes',
            'subcategories',
            'categories',
            'slug'
        ]


class CollectionSerializer(serializers.ModelSerializer):
    image = ImageSerializer(required=False, read_only=True)
    items = ItemSerializer(required=False, read_only=True, many=True)

    class Meta:
        model = Collection
        fields = [
            'id',
            'name',
            'description',
            'slug',
            'image',
            'items',
            'featured'
        ]


class MiniCollectionSerializer(serializers.ModelSerializer):
    image = ImageSerializer(required=False, read_only=True)

    class Meta:
        model = Collection
        fields = [
            'id',
            'name',
            'description',
            'slug',
            'image',
            'featured'
        ]


class OfferSerializer(serializers.ModelSerializer):
    image = ImageSerializer(required=False, read_only=True)
    subcategory = SubCategorySerializer(
        required=False, read_only=True)

    class Meta:
        model = Offer
        fields = [
            'id',
            'title',
            'slug',
            'category',
            'subcategory',
            'item',
            'collection',
            'image'
        ]
