from django.db import models

# Create your models here.
class login(models.Model):
    emailid=models.CharField(max_length=30,primary_key=True)
    password=models.CharField(max_length=10)

class signup(models.Model):
    firstname=models.CharField(max_length=15)
    lastname=models.CharField(max_length=10)
    emailid=models.CharField(max_length=30,primary_key=True)
    password=models.CharField(max_length=10)
    dobd=models.CharField(max_length=2)
    dobm=models.CharField(max_length=5)
    doby=models.CharField(max_length=4)
    gender=models.CharField(max_length=6)
    displayimage=models.ImageField(upload_to='images/')

class post(models.Model):
    id=models.IntegerField(primary_key=True)
    userid=models.ForeignKey(signup, on_delete=models.CASCADE)
    posttitle=models.CharField(max_length=100)
    postimage=models.ImageField(upload_to='images/')
    date=models.DateTimeField(auto_now_add=True)
    location=models.CharField(max_length=50)
    activity=models.CharField(max_length=30)


class like(models.Model):
    postid = models.ForeignKey(post, on_delete=models.CASCADE)
    userid = models.ForeignKey(signup, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = (('postid','userid'),)
class comment(models.Model):
    postid = models.ForeignKey(post, on_delete=models.CASCADE)
    userid = models.ForeignKey(signup, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    commenttext=models.CharField(max_length=100)
class friendslist(models.Model):
    sender  = models.ForeignKey(signup, on_delete=models.CASCADE,related_name="sender")
    reciever = models.ForeignKey(signup, on_delete=models.CASCADE,related_name="reciever")
    reqstatus = models.CharField(max_length=100)
    class Meta:
        unique_together = (('sender','reciever'),)

class message(models.Model):
    sender  = models.ForeignKey(signup, on_delete=models.CASCADE,related_name="messagesender")
    reciever = models.ForeignKey(signup, on_delete=models.CASCADE,related_name="messagereciever")
    date = models.DateTimeField(auto_now_add=True)
    messagetext=models.CharField(max_length=100)

