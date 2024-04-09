from django.shortcuts import render,redirect
from django.core.paginator import Paginator
from userapp.models import*
from adminapp.models import*
from datetime import datetime


# Create your views here.


def mining_dashboard(req):
    scan = ScannedVehicle.objects.all().count()
    current_datetime = datetime.now()
    
    # Get the aggregate data for all companies
    total_logins = 0
    last_login_date = None
    for company in Company.objects.all():
        total_logins += company.no_of_times_login
        if not last_login_date or company.last_login_date > last_login_date:
            last_login_date = company.last_login_date

    return render(req, 'mining/admin-dashboard.html', {
        'scan': scan,
        'current_datetime': current_datetime,
        'total_logins': total_logins,
        'last_login_date': last_login_date
    })



def mining_allusers(req):
    y = ScannedVehicle.objects.all()
    paginator = Paginator(y, 5) 
    page_number = req.GET.get('page')
    post = paginator.get_page(page_number)
    return render(req,'mining/admin-allusers.html', {'vehicles':post})


