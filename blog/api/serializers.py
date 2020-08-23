from rest_framework import serializers
from blog.models import (
    Post,
    Category,
    Group,
    Tag,
    Rating,
    Quote,
    Image,
    Question,
    BodyImage
)
from accounts.models import MyUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = [
            'id',
            'username',
            'first_name',
            'last_name'
        ]


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = [
            'name',
            'slug',
            'description'
        ]


class CategorySerializer(serializers.ModelSerializer):
    group = GroupSerializer(required=False, read_only=True)

    class Meta:
        model = Category
        fields = [
            'name',
            'banner_xlarge',
            'banner_large',
            'banner_nslarge',
            'banner_normal',
            'banner_medium',
            'banner_small',
            'banner_xsmall',
            'description',
            'main',
            'slug',
            'group',
        ]


class WriterCategorySerializer(serializers.ModelSerializer):
    group = GroupSerializer(required=False, read_only=True)

    class Meta:
        model = Category
        fields = [
            'name',
            'banner_xlarge',
            'banner_large',
            'banner_nslarge',
            'banner_normal',
            'banner_medium',
            'banner_small',
            'banner_xsmall',
            'description',
            'main',
            'slug',
            'group',
            'post_set',
            'created_date'
        ]


class MiniCategorySerializer(serializers.ModelSerializer):
    group = GroupSerializer(required=False, read_only=True)

    class Meta:
        model = Category
        fields = [
            'name',
            'description',
            'main',
            'slug',
            'group'
        ]


class AddCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = [
            'name',
            'banner_xlarge',
            'banner_large',
            'banner_nslarge',
            'banner_normal',
            'banner_medium',
            'banner_small',
            'banner_xsmall',
            'description',
            'main',
        ]


class EditCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = [
            'description',
            'main',
        ]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = [
            "name",
            "slug",
        ]


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = [
            'rating',
            'total_reviews',
            'rating_sum'
        ]


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = [
            'id',
            'post',
            'caption_title',
            'caption_body',
            'image_xlarge',
            'image_large',
            'image_nslarge',
            'image_normal',
            'image_medium',
            'image_small',
            'image_xsmall'
        ]


class AddImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = [
            'post',
            'image_xlarge',
            'image_large',
            'image_nslarge',
            'image_normal',
            'image_medium',
            'image_small',
            'image_xsmall',
            'caption_title',
            'caption_body'
        ]


class EditImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = [
            'post',
            'caption_title',
            'caption_body'
        ]


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = [
            'id',
            'question',
            'answer'
        ]


class AddQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = [
            'question',
            'answer'
        ]


class QuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quote
        fields = [
            'id',
            'body',
            'author',
            'created_date'
        ]


class PostSerializer(serializers.ModelSerializer):
    category = CategorySerializer(required=False, read_only=True)
    tag_set = TagSerializer(required=False, read_only=True, many=True)
    rating = RatingSerializer(required=False, read_only=True)
    image_set = ImageSerializer(required=False, read_only=True, many=True)
    question_set = QuestionSerializer(
        required=False, read_only=True, many=True)

    class Meta:
        model = Post
        fields = [
            'id',
            'writer',
            'banner_xlarge',
            'banner_large',
            'banner_nslarge',
            'banner_normal',
            'banner_medium',
            'banner_small',
            'banner_xsmall',
            'title',
            'description',
            'body',
            'structure',
            'created_date',
            'image_set',
            'category',
            'slug',
            'tag_set',
            'rating',
            'question_set',
            'featured',
            'views'
        ]


class AddPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = [
            'title',
            'writer',
            'description',
            'body',
            'structure',
            'banner_xlarge',
            'banner_large',
            'banner_nslarge',
            'banner_normal',
            'banner_medium',
            'banner_small',
            'banner_xsmall',
            'featured'
        ]


class EditPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = [
            'description',
            'writer',
            'body',
            'structure',
            'featured'
        ]


class MiniPostSerializer(serializers.ModelSerializer):
    category = MiniCategorySerializer(required=False, read_only=True)

    class Meta:
        model = Post
        fields = [
            'id',
            'writer',
            'banner_xlarge',
            'banner_large',
            'banner_nslarge',
            'banner_normal',
            'banner_medium',
            'banner_small',
            'banner_xsmall',
            'title',
            'description',
            'created_date',
            'category',
            'slug',
            'structure',
            'image_set'
        ]


class SearchPostSerializer(serializers.ModelSerializer):
    category = MiniCategorySerializer(required=False, read_only=True)

    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'category',
            'slug'
        ]


class WriterSearchPostSerializer(serializers.ModelSerializer):
    category = MiniCategorySerializer(required=False, read_only=True)
    rating = RatingSerializer(required=False, read_only=True)

    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'category',
            'rating',
            'created_date',
            'slug',
            'structure',
            'featured',
            'views'
        ]


class BodyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BodyImage
        fields = [
            'upload',
            'upload_nslarge',
            'upload_normal',
            'upload_medium',
            'upload_small',
        ]
