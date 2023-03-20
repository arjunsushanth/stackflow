from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
    title=models.CharField(max_length=200)
    description=models.CharField(max_length=200)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    image=models.ImageField(upload_to="images",null=True)
    date=models.DateField(auto_now_add=True)
    def __str__(self):
        return self.title
    @property
    def question_answers(self):
        return self.answers_set.all()

class Answers(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    question=models.ForeignKey(Question,on_delete=models.CASCADE)
    answer=models.CharField(max_length=200)
    date=models.DateField(auto_now_add=True)
    upvote=models.ManyToManyField(User,related_name="upvotes")
    def __str__(self):
        return self.answer
    @property
    def upvote_count(self):
        return self.upvote.all().count()




# Create your models here.
