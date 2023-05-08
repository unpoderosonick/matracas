from django.shortcuts import render
from core.models import Activity, Visit
from django.db.models.functions import ExtractWeek, ExtractYear
from django.db.models import Sum, F
from datetime import datetime, timedelta

def get_date_from_week(year, week_number):
    # Calculate the start of the week
    start_of_week = datetime.strptime(f'{year}-W{week_number-1}-1', '%Y-W%W-%w').date()

    # Calculate the end of the week
    end_of_week = start_of_week + timedelta(days=6)

    return start_of_week, end_of_week


def report(request):
    activities = Activity.objects.all().order_by('name')
    
    stats = (Visit.objects        
        .annotate(year=ExtractYear('visited_at'))
        .annotate(week=ExtractWeek('visited_at'))
        .values('year', 'week')
        .annotate(sum_cattle=Sum('cattle'))
        .annotate(sum_sheep=Sum('sheep'))
        .annotate(sum_alpacas=Sum('alpacas'))
        .annotate(sum_llamas=Sum('llamas'))
        .annotate(sum_canes=Sum('canes'))
        .annotate(sum_animals=Sum(F('cattle') + F('sheep') + F('alpacas') + F('llamas')+ F('canes')))
    )
    
    year = 2023
    result = []
    for s in stats:
        # print('s------------------- ')
        # print(s)
        week_number = s['week']
        start_of_week, end_of_week = get_date_from_week(year, week_number)
        result.append({'start_of_week':start_of_week, 'data': s})
        s[start_of_week] = start_of_week
        s[end_of_week] = end_of_week

    # print('stats--------------')
    # print(stats)
    return render(request, 'dashboard/home.html', locals())
