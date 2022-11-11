
from django.shortcuts import render
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import *

from .models import Fixture,MatchesPredictions,MatchPoint
from user.models import MyUser

from django.utils import timezone

from .task import Epl_today_fixtures,Fixtures_stats,point_reset,winner_point,send_mail_func


def fixtures(request):
    if request.user.is_anonymous:
        messages.error(request,'You must log in to view the content.')
        return redirect('/')
    else:
        return fixtures2(request)

@login_required
def fixtures2(request):
    print(request.build_absolute_uri )
    fixtures = MatchesPredictions.objects.filter(user=request.user,match__fulltime=False,match__matchtime__gt=timezone.localtime(timezone.now()))
    # fixtures = Fixture.objects.filter(fulltime=False,matchtime__gt=timezone.localtime(timezone.now()))
    username = MyUser.objects.get(user=request.user)
    context = {'fixtures':fixtures,
                    'user':username
                    }
    return render(request,"league/fixture.html",context)

    # return render(request,"league/fixture.html",)

def Predictions(request,pk):
    if request.user.is_anonymous:
        messages.error(request,'You must log in to view the content.')
        return redirect('/')
    else:
        return Predictions2(request,pk)


@login_required
def Predictions2(request,pk):
    if MatchesPredictions.objects.filter(user=request.user,match=pk,has_predicated=False).exists():
        fixture = MatchesPredictions.objects.get(user=request.user,match=pk,has_predicated=False)
        if request.method == 'GET':
            if fixture.match.matchtime >= timezone.localtime(timezone.now()):  # type: ignore
                othersprediction = MatchesPredictions.objects.filter(match=pk)
                context = {'fixture' : fixture,'othersprediction':othersprediction}
                return render(request,'league/fixturePredictions.html',context)
            else:
                messages.error(request,"Prediction time's up")
                return redirect('/authuser/fixtures')
                
        if request.method == 'POST':
            if fixture.match.matchtime >= timezone.localtime(timezone.now()):  # type: ignore
                pridction = request.POST.get('selector')
                fixture.userprediction = pridction
                fixture.has_predicated =  True
                fixture.save()
                messages.error(request,'Prediction Saved')
                return redirect('/authuser/fixtures')
            else:
                messages.error(request,"Prediction time's up")
                return redirect('/authuser/fixtures')
    elif MatchesPredictions.objects.filter(user=request.user,match=pk,has_predicated=True).exists():
        othersprediction = MatchesPredictions.objects.filter(match=pk)
        thisfixture = Fixture.objects.get(id=pk)
        context = {'othersprediction':othersprediction,'fixture':thisfixture}
        return render(request,'league/othersPredictions.html',context)
    else:
        messages.error(request,"Sorry you're not registered for this matchday ")
        return redirect('/authuser/fixtures')

    

    
    


def tableview(request):
    if request.user.is_anonymous:
        messages.error(request,'You must log in to view the content.')
        return redirect('/')
    else:
        return tableview2(request)

@login_required
def tableview2(request):
    userrank = MyUser.objects.all().order_by('-point')
    context = {'userrank' : userrank}
    return render(request,'league/tableview.html',context)


def PastPredictions(request):
    if request.user.is_anonymous:
        messages.error(request,'You must log in to view the content.')
        return redirect('/')
    else:
        return PastPredictions2(request)

@login_required
def PastPredictions2(request):
    predictions = MatchPoint.objects.filter(Fixture__user = request.user)
    context = {'predictions' : predictions}
    return render(request,'league/predictions.html',context)
    

