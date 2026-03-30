from django.shortcuts import render
from .models import NetworkLog, Alert
# Create your views here.


def dashboard(request):
    company = request.user.userprofile.company

    logs = NetworkLog.objects.filter(company=company).order_by('timestamp')[:50]
    alerts = Alert.objects.filter(company=company).order_by('-timestamp')[:20]

    return render( request, "dashboard.html", {
        "logs": logs,
        "alerts": alerts
    })

