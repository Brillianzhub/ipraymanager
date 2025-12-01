# app/serializers.py
from rest_framework import serializers
from .models import TemplateTag, ShareTemplate


class TemplateTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemplateTag
        fields = ('id', 'name', 'description')


class TemplateSerializer(serializers.ModelSerializer):
    """
    Serializer for Template model
    """

    class Meta:
        model = ShareTemplate
        fields = [
            'id',
            'name',
            'template_type',
            'gradient_colors',
            'background',
            'text_color',
            'styles',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_gradient_colors(self, value):
        """Validate gradient colors list"""
        if not isinstance(value, list):
            raise serializers.ValidationError("Must be a list of colors")

        if len(value) == 0:
            raise serializers.ValidationError("At least one color is required")

        return value

    def validate_text_color(self, value):
        """Validate text color format"""
        if not value.startswith('#'):
            value = f"#{value}"

        if len(value) not in [7, 4]:  # #RRGGBB or #RGB
            raise serializers.ValidationError("Must be a valid hex color code")

        return value

    def validate_background(self, value):
        """Validate background color format"""
        if value:
            if not value.startswith('#'):
                value = f"#{value}"

            if len(value) not in [7, 4]:  # #RRGGBB or #RGB
                raise serializers.ValidationError(
                    "Must be a valid hex color code")

        return value

    def validate_styles(self, value):
        """Validate styles dictionary"""
        if not isinstance(value, dict):
            raise serializers.ValidationError(
                "Must be a dictionary of style definitions")

        return value


class TemplateListSerializer(serializers.ModelSerializer):
    """
    Minimal serializer for template list view
    """

    class Meta:
        model = ShareTemplate
        fields = [
            'id',
            'name',
            'template_type',
            'created_at'
        ]
