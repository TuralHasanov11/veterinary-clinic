from rest_framework import serializers
from .models import Medicine, MedicineCompany

class MedicineCompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = MedicineCompany
        fields = '__all__'


class MedicineSerializer(serializers.ModelSerializer):
    total_price = serializers.ReadOnlyField()
    our_total_price = serializers.ReadOnlyField()
    company = MedicineCompanySerializer(many=False)
    
    class Meta:
        model = Medicine
        fields = '__all__'


class MedicineCreateUpdateSerializer(serializers.ModelSerializer):
    total_price = serializers.ReadOnlyField()
    our_total_price = serializers.ReadOnlyField()
    class Meta:
        model = Medicine
        fields = '__all__'



