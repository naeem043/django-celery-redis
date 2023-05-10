from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .tasks import update_inactive_users
from django_celery_beat.models import PeriodicTask, CrontabSchedule
from django.core.cache import cache
from django.contrib.auth.models import User

def update_user(request):
    update_inactive_users.delay()
    
    return HttpResponse("updated")

def dynamically_run_task(request):
    # the CrontabSchedule and PeriodicTask parameters will find here: https://docs.celeryq.dev/en/stable/reference/celery.schedules.html
    hour, minute = 11, 20
    schedule, created = CrontabSchedule.objects.get_or_create(hour = hour, minute = minute)
    task = PeriodicTask.objects.create(crontab=schedule, name="update_inactive_users_"+str(schedule.id), task='user.tasks.update_inactive_users')#, args = json.dumps([[2,3]]))
    return HttpResponse("Done")


def redis_cache(request):
    '''
        documentations: https://docs.djangoproject.com/en/4.1/topics/cache/
        additional documentation https://github.com/jazzband/django-redis
    '''

    src, users = "", []
    if cache.get('user_list'):
        users = cache.get('user_list')
        src = 'redis'
        cache.touch('user_list', timeout = 20) #touch is use for overwrite previous cahce rules, 
        
        # cache.delete('a') #delete one cache
        # cache.delete_many(['a', 'b', 'c']) #delete multi caches
    else:
        users = list(User.objects.values().filter(is_active=True))*100
        cache.set('user_list',users, timeout = 20) 
        src = 'db'  
    data = {
        "ttl":cache.ttl('user_list'),
        "pttl":cache.pttl('user_list'),
        "persist":cache.persist('user_list'),
        "src":src,
        "users":users,
    }
    return JsonResponse(data)