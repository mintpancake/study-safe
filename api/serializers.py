from rest_framework import serializers
from .models import *


class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        fields = '__all__'


class HkuMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = HkuMember
        fields = '__all__'


class VisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visit
        fields = '__all__'
