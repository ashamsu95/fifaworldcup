from django.urls import path
from . import views

app_name= 'league_app'
urlpatterns = [
        path('fixtures',views.fixtures,name='fixtures'),
        path('leaguetable',views.tableview,name='leaguetable'),
        path('userspridctions/<int:pk>',views.Predictions,name='userpridction'),
        path('PastPredictions',views.PastPredictions,name='PastPredictions')
]