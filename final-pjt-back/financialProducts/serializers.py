from rest_framework import serializers
from .models import DepositProducts, DepositOptions

class DepositProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositProducts
        fields = '__all__'
    
    class DepositOptionsListSerializer(serializers.ModelSerializer):
        class Meta:
            model = DepositOptions
            fields = '__all__'

    depositoptions_set = DepositOptionsListSerializer(many=True, read_only=True)
    
    

class DepositOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositOptions
        fields = '__all__'
        read_only_field = ('product',)