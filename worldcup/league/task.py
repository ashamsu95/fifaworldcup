import requests
from celery.schedules import crontab

from celery import shared_task
from django_celery_beat.models import PeriodicTask, CrontabSchedule


import json
from types import SimpleNamespace

from django.utils import timezone
from datetime import datetime
import zoneinfo
from datetime import timedelta

import random
from .models import Fixture

from user.models import MyUser




headers = { 'X-Auth-Token': 'ad2a3f6ccd9349b193a72df349c0d94f' }


def formatter(di):
    if "utcDate" in di:
        dateandtime = di["utcDate"]
        return  dateandtime 
    if "id" in di:
        ids = di["id"]
        return  ids
    elif "awayTeam" in di:
        away_name = di["awayTeam"]["name"]
        away_name_img = di["awayTeam"]["crest"]
        return {"name":away_name,"img":away_name_img}
    elif "homeTeam" in di:
        home_name = di["homeTeam"]["name"]
        home_name_img = di["homeTeam"]["crest"]
        return {"name":home_name,"img":home_name_img}

def convert_to_localtime(utctime):
    utc= datetime.strptime(utctime,'%Y-%m-%dT%H:%M:00Z').replace(tzinfo=zoneinfo.ZoneInfo("UTC"))
    current_tz = timezone.get_current_timezone()
    local = utc.astimezone(current_tz)
    return local





@shared_task(bind=True)
def winner_point(self):
    uri = 'http://api.football-data.org/v4/matches/391944'
    headers = { 'X-Auth-Token': 'ad2a3f6ccd9349b193a72df349c0d94f' }
    response = requests.get(uri, headers=headers)
    in_data = json.loads(response.content,object_hook=lambda d: SimpleNamespace(**d))
    in_data = json.loads(response.content,object_hook=lambda d: SimpleNamespace(**d))
    winner=in_data.season.winner
    users = MyUser.objects.filter(team__iexact=winner)
    for user in users:
        user.point = user.point + 10
        user.save()
    return "winner point"


@shared_task(bind=True)
def point_reset(self):
    users = MyUser.objects.all()
    for user in users:
        user.point = 0
        user.save()
    
    return "poin reset"

@shared_task(bind=True)
def Epl_today_fixtures(self,date,comp):
    Epl_Url = 'https://api.football-data.org/v4/competitions/'+str(comp)+'/matches'
    body={
        'dateFrom':date,
        'dateTo':date,
        }
    response = requests.get(Epl_Url, headers=headers,params=body)
    in_data = response.json()["matches"]
    match_data_table = []
    for match_info in in_data:
        di = {str(x):formatter({str(x) : match_info[x]}) for x in ["id","utcDate","homeTeam", "awayTeam"]}
        match_data_table.append(di)
    
    if len(match_data_table) !=  0:
       for matches in match_data_table:
        newmatch = Fixture.objects.create(
            matchid = matches["id"],
            Home = matches["homeTeam"]["name"],
            Away = matches["awayTeam"]["name"],
            homeimg= matches["homeTeam"]["img"],
            awayimg= matches["awayTeam"]["img"],
            matchtime= convert_to_localtime(matches["utcDate"]),
        )
        matchends = convert_to_localtime(matches["utcDate"])+ timedelta(hours=2,minutes=1)
        schedule, created = CrontabSchedule.objects.get_or_create(hour = matchends.hour, minute = matchends.minute, month_of_year =matchends.month, day_of_month=matchends.day)
        task = PeriodicTask.objects.create(crontab=schedule, name=matches["homeTeam"]["name"]+" vs " +matches["awayTeam"]["name"] , task='league.task.Fixtures_stats',args =json.dumps([matches["id"],]))


    return "Done"


# here we are converting json into objects more easy 
@shared_task(bind=True)
def Fixtures_stats(self,matchid):
    uri = 'http://api.football-data.org/v4/matches/'+str(matchid)
    headers = { 'X-Auth-Token': 'ad2a3f6ccd9349b193a72df349c0d94f' }
    response = requests.get(uri, headers=headers)
    in_data = json.loads(response.content,object_hook=lambda d: SimpleNamespace(**d))
    fixture_id = Fixture.objects.get(matchid=matchid)
    if in_data.status == "FINISHED":
        if in_data.score.winner == "HOME_TEAM":
            fixture_id.result = "Home"
        elif in_data.score.winner == "DRAW":
            fixture_id.result = "draw"
        elif in_data.score.winner == "AWAY_TEAM":
            fixture_id.result = "Away"
        fixture_id.Score = str(fixture_id.Home) +" " +str(in_data.score.fullTime.home)+" - "+str(in_data.score.fullTime.away)+" " +str(fixture_id.Away) 
        fixture_id.fulltime = True
        fixture_id.save()
    elif in_data.status == "IN_PLAY" or in_data.status == "PAUSED":
        matchends = fixture_id.matchtime + timedelta(hours=3,minutes=15)
        schedule, created = CrontabSchedule.objects.get_or_create(hour = matchends.hour, minute = matchends.minute, month_of_year =matchends.month, day_of_month=matchends.day)
        task = PeriodicTask.objects.create(crontab=schedule, name=fixture_id.Home+" vs " +fixture_id.Away+str(random.randrange(1,100)), task='league.task.Fixtures_stats',args =json.dumps([matchid,]))
        return "Done"
    elif in_data.status == "SUSPENDED" or in_data.status == "POSTPONED":
        return "Done"



