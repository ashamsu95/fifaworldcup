from turtle import home
from django.db import models
from django.contrib.auth.models import User

from user.models import MyUser
from django.db.models.signals import post_save
from django.dispatch import receiver



class Fixture(models.Model):
    matchid = models.IntegerField(null=True,blank=True)
    Home = models.CharField(max_length=30)
    Away = models.CharField(max_length=30)
    result =  models.CharField(max_length=30,blank=True)
    Score = models.CharField(max_length=50,blank=True)
    fulltime = models.BooleanField(default=False)
    homeimg=models.CharField(max_length=200,blank=True)
    awayimg=models.CharField(max_length=200,blank=True)
    matchtime=models.DateTimeField(null=True,blank=True)
    
    def __str__(self):
        return self.Home + ' vs ' + self.Away

class MatchesPredictions (models.Model):
    match = models.ForeignKey(Fixture, on_delete=models.CASCADE)
    class Prediction(models.TextChoices):
        Home = 'Home'
        Away = 'Away'
        draw ='draw'
        no_Prediction ='non'
       
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    userprediction = models.CharField(max_length=30,choices=Prediction.choices,default=Prediction.no_Prediction)

    def __str__(self):
        return self.match.Home +' vs '+ self.match.Away +" "+ self.user.username+"'s prediction"

class MatchPoint(models.Model):
    # user = models.OneToOneField(User,on_delete=models.CASCADE)
    point = models.IntegerField(blank=True)
    Fixture = models.OneToOneField(MatchesPredictions,on_delete=models.CASCADE)

    def __str__(self):
        return self.Fixture.user.username +" "+ self.Fixture.match.Home + ' vs ' + self.Fixture.match.Away


@receiver(post_save,sender=Fixture)
def create_MatchesPredictions(sender,instance,created,**kwargs):
    users = User.objects.all()
    if created:
        for u in users:
            MatchesPredictions.objects.create(match=instance,user=u)
    if created == False:
        if instance.fulltime == True:
            fixture_prediction = MatchesPredictions.objects.filter(match=instance)
            for fix in fixture_prediction:
                user_point_update=MyUser.objects.get(user=fix.user)
                if fix.userprediction == 'non':
                    MatchPoint.objects.create(point=1,Fixture=fix)
                    user_point_update.point = user_point_update.point +1
                    user_point_update.save()
                elif fix.userprediction == instance.result:
                    MatchPoint.objects.create(point=3,Fixture=fix)
                else:
                    MatchPoint.objects.create(point=-1,Fixture=fix)
                    