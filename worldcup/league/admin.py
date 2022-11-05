from django.contrib import admin
from .models import MatchPoint,MatchesPredictions,Fixture
# Register your models here.

admin.site.register(MatchPoint)
admin.site.register(MatchesPredictions)
admin.site.register(Fixture)