from django.db import models
from django.contrib.auth.models import User



class MyUser(models.Model):
    class Team(models.TextChoices):
        Uruguay = 'Uruguay',
        Germany ="Germany",       
        Spain ="Spain",
        Argentina ="Argentina",     
        Ghana ="Ghana",
        Brazil ="Brazil",        
        Portugal ="Portugal",      
        Japan ="Japan",
        Mexico ="Mexico",        
        England ="England",       
        United_States ="United States", 
        Korea_Republic ="Korea Republic",
        France ="France",        
        Australia ="Australia",     
        Serbia ="Serbia",        
        Cameroon ="Cameroon",      
        Denmark ="Denmark",       
        Switzerland ="Switzerland",   
        Ecuador ="Ecuador",
        Costa_Rica ="Costa_Rica",
        Poland ="Poland",
        Croatia ="Croatia",
        Saudi_Arabia ="Saudi Arabia",
        Tunisia ="Tunisia",
        Senegal ="Senegal",
        Belgium ="Belgium",
        Morocco ="Morocco",
        Canada ="Canada",
        Wales ="Wales",
        Iran ="Iran",
        Qatar ="Qatar",
        Netherlands ="Netherlands",                

        def __str__(self):
            return self.name

    phone = models.IntegerField(default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    point = models.IntegerField(default=0)
    team = models.CharField(max_length=30,choices=Team.choices,default=Team.Japan)

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name
#

class addduser_number(models.Model):
    phone = models.IntegerField(default=0)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    alreadyuser = models.BooleanField(default=False)
    def __str__(self):
        return str(self.phone) +' added by ' + self.user.first_name + ' ' + self.user.last_name