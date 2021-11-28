from django.db import models
from django.contrib.auth.models import User


class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    USERNAME_FIELD='user'
    def __str__(self):
         return self.user

class Chat(models.Model):
    end1 = models.ForeignKey(Person,on_delete=models.CASCADE, related_name='end1')
    end2 = models.ForeignKey(Person,on_delete=models.CASCADE, related_name='end2')
    content = models.TextField(max_length=100000)
    allowed = models.BooleanField(default=True)

class Course(models.Model):
    educator = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='educator')
    name = models.CharField(max_length=150, blank=False)
    ta = models.ManyToManyField(Person,null=True,blank=True,related_name='ta')
    students = models.ManyToManyField(Person,null=True,blank=True,related_name='students')
    chat_allowed = models.BooleanField(default=True)
    mem_ta_allowed = models.BooleanField(default=False)
    create_ta_allowed = models.BooleanField(default=False)
    chat_content = models.TextField(max_length=100000, default='')

class Announcements(models.Model):
    crs = models.ForeignKey(Course, on_delete=models.CASCADE)
    content = models.CharField(max_length=10000)


class Work(models.Model):
    crs = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    total_marks = models.IntegerField()
    deadline = models.DateTimeField(null=True)
    ##############################################
    weightage = models.IntegerField(null=True)
    def __str__(self):
        return self.name

class Graded(models.Model):
    work=models.ForeignKey(Work, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    path = str(work.name)+'/graded_csv/'
    submission = models.FileField(upload_to = path)

    def __str__(self):
        return self.name

class Grader_sh(models.Model):
    work=models.ForeignKey(Work, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    path = str(work.name)+'/graded_csv/'
    submission = models.FileField(upload_to = path)

    def __str__(self):
        return self.name
        
class Assignment(models.Model):
    work = models.ForeignKey(Work, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    obtained_marks = models.IntegerField()
    path = str(work.name)+'/submissions/'
    submission = models.FileField(upload_to = path)

    def __str__(self):
        return self.name





