"""
Serializers required for Helplines
"""

from rest_framework import serializers
from .models import HelpLine

class HelplineSerializer(serializers.ModelSerializer):
    """
    Serializer for Helper model
    """
    class Meta:
        """
        Meta class to specify the serializer attributes
        """
        model = HelpLine
        fields = ("name", "helpline_number",)