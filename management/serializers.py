"""
Serializers required for Helplines
"""

from rest_framework import serializers
from .models import HelpLine,HelperCategory

class HelplineSerializer(serializers.ModelSerializer):
    """
    Serializer for Helpline model
    """
    class Meta:
        """
        Meta class to specify the serializer attributes
        """
        model = HelpLine
        fields = ("name", "helpline_number",)

class HelperCategorySerializer(serializers.ModelSerializer):
    """
    Serializer for Helper model
    """
    class Meta:
        """
        Meta class to specify the serializer attributes
        """
        model = HelperCategory
        fields = ("name",)