from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets
from api.serilizer import UserSerilizer,QuestionSerilizer,AnswerSerilizer,serializers
from rest_framework import authentication,permissions
from api.models import Question,Answers
from rest_framework.decorators import action

class UserView(viewsets.ViewSet):
    def create(self,request,*args,**kwargs):
        serilizer=UserSerilizer(data=request.data)
        if serilizer.is_valid():
            serilizer.save()
            return Response(data=serilizer.data)
        else:
            return Response(data=serilizer.errors)

class QuestionView(viewsets.ModelViewSet):
    serializer_class=QuestionSerilizer
    queryset=Question.objects.all()
    #authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serilizer=QuestionSerilizer(data=request.data)
        if serilizer.is_valid():
            serilizer.save(user=request.user)
            return Response(data=serilizer.data)
        else:
            return Response(serilizer.errors)
    def get_queryset(self):
        return Question.objects.all().exclude(user=self.request.user)

    # def list(self, request, *args, **kwargs):
    #     qs=Question.objects.all().exclude(user=request.user)
    #     serilizer=QuestionSerilizer(qs,many=True)
    #     return Response(data=serilizer.data)
    

    @action(methods=["POST"],detail=True)
    def add_answer(self,request,*args,**kwargs):
         id=kwargs.get("pk")
         object=Question.objects.get(id=id)
         serilizer=AnswerSerilizer(data=request.data)
         if serilizer.is_valid():
            serilizer.save(user=request.user,question=object)
            return Response(data=serilizer.data)
         else:
            return Response(data=serilizer.errors)

class AnswerView(viewsets.ModelViewSet):
    serializer_class=AnswerSerilizer
    queryset=Answers.objects.all()
    #authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        raise serializers.ValidationError("METHOD NOT ALLOWED")  
    def list(self, request, *args, **kwargs):
        raise serializers.ValidationError("METHOD NOT ALLOWED") 

    def destroy(self, request, *args, **kwargs):
        object=self.get_object()
        if request.user==object.user:
            object.delete()
            return Response(data="deleted")
        else:
            raise serializers.ValidationError("permission denied for this user")   

    @action(methods=["POST"],detail=True)
    def add_upvote(self,requst,*args,**kwargs):
        object=self.get_object()  
        user=requst.user
        object.upvote.add(user)
        return Response(data="up vote")   
     
            
        


        

