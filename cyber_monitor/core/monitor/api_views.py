from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import NetworkLog, Alert
from .serializers import NetworkLogSerializer, AlertSerializer

#----------------
# Multi-tenant API
#----------------


@api_view(['GET'])
@permission_classes([IsAuthenticated])

def get_logs(request):
    """
    Return latest alert for the company of the authenticated user.
    """

    company = request.user.userprofile.company
    logs = NetworkLog.objects.filter(company=company).order_by('-timestamp')[:50]
    serializer = AlertSerializer(logs, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])

def get_alerts(request):
    """
    Return latest alert for the company of the authenticated user.
    """

    company = request.user.userprofile.company
    alerts = Alert.objects.filter(company=company).order_by('-timestamp')[:50]
    serializer = AlertSerializer(alerts, many=True)
    return Response(serializer.data)