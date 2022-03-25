from django.urls import path
from auction import views

urlpatterns = [

    path('login', views.userlogin, name = 'login'),
    path('logout', views.logout_user, name = 'logout'),
    path('changepassword', views.changepassword, name = 'changepassword'),

    path('', views.test, name = 'home'),

    ## API
    path('startRound', views.startRound, name = 'startRound'),
    path('bidparticipation/<str:varRound>', views.bidparticipation, name = 'bidparticipation'),
    path('endround/<str:varRound>', views.endround, name = 'endround'),

    
]