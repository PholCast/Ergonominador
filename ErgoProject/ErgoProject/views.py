from django.http import JsonResponse
from mqttApp.models import Alert
from django.shortcuts import render

def get_alerts(request):
    # Aquí podríamos filtrar por alertas recientes si es necesario
    alerts = Alert.objects.order_by('-created_at')[:10]  # Últimas 10 alertas
    alert_data = [{"type_alert": alert.type_alert, "message": alert.message, "created_at": alert.created_at} for alert in alerts]
    return JsonResponse(alert_data, safe=False)


def dashboard_view(request):
    return render(request, "dashboard.html") 