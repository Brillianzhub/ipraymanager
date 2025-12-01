from django.utils.text import slugify
from rest_framework import serializers
from .models import Blog, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class BlogSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(
        read_only=True)  # show username instead of id
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field="name"  
    )

    class Meta:
        model = Blog
        fields = "__all__"

    def generate_unique_slug(self, title, instance=None):
        base_slug = slugify(title)
        slug = base_slug
        counter = 1
        qs = Blog.objects.all()
        if instance:
            qs = qs.exclude(pk=instance.pk)
        while qs.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        return slug

    def create(self, validated_data):
        # always generate slug from title
        validated_data["slug"] = self.generate_unique_slug(
            validated_data["title"])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if "title" in validated_data:
            # regenerate slug whenever title changes
            validated_data["slug"] = self.generate_unique_slug(
                validated_data["title"], instance=instance)
        return super().update(instance, validated_data)


class BlogListSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    category = serializers.StringRelatedField()

    class Meta:
        model = Blog
        fields = (
            "id",
            "author",
            "category",
            "title",
            "description",
            "slug",
            "publish",
            "image",
            "featured",
            "read_time",
        )
