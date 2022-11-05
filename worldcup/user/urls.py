from django.urls import path
from . import views

app_name= 'user_app'
urlpatterns = [
        path('',views.loginuser,name='login'),
        path('register',views.register_page,name='register'),
        path('logout',views.logout_page,name='logout'),
        path('addphone',views.addnumber,name='addnumber')
]