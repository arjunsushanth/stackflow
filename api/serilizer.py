from rest_framework import serializers
from django.contrib.auth.models import User
from api.models import Question,Answers

class UserSerilizer(serializers.ModelSerializer):

    class Meta:
        model=User
        fields=["username","email","password"]
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
class QuestionSerilizer(serializers.ModelSerializer):
    user=serializers.CharField(read_only=True)
    date=serializers.CharField(read_only=True)
    
    class Meta:
        model=Question
        fields="__all__"
class AnswerSerilizer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    user=serializers.CharField(read_only=True)
    question=serializers.CharField(read_only=True)
    upvote=serializers.CharField(read_only=True)
    upvote_count=serializers.CharField(read_only=True)
    class Meta:
        model=Answers
        fields="__all__"