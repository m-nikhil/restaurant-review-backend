from . import models
from rest_framework import serializers
from datetime import datetime

class ReviewGetSerializer(serializers.ModelSerializer):
    postedTime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S %Z")
    postedByEmail = serializers.CharField(source='postedBy.email')
    class Meta:
        model = models.Review
        fields = ('id','review', 'postedByEmail', 'postedTime') 


class ReviewPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Review
        fields = ('review',)

    def create(self, validated_data):
        postedBy = self.context['request'].user
        postedTime = datetime.now()
        return models.Review.objects.create(postedBy=postedBy,postedTime=postedTime,**validated_data)

class ReviewPutSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Review
        fields = ('id','review')