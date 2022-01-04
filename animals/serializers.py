from rest_framework import serializers
from .models import Feed, Doctor, MedicalExamination

class FeedSerializer(serializers.ModelSerializer):
    total_weight = serializers.ReadOnlyField()

    class Meta:
        model = Feed
        fields = '__all__'


class DoctorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Doctor
        fields = '__all__'


class MedicalExaminationSerializer(serializers.ModelSerializer):
    price = serializers.ReadOnlyField()

    class Meta:
        model = MedicalExamination
        fields = '__all__'