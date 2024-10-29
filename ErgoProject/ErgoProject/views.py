from django.http import JsonResponse
from mqttApp.models import Alert, SensorLuz, SensorSonido, SensorTemp, Postura
from django.shortcuts import render

def get_alerts(request):
    # Aquí podríamos filtrar por alertas recientes si es necesario
    alerts = Alert.objects.order_by('-created_at')[:10]  # Últimas 10 alertas
    alert_data = [{"type_alert": alert.type_alert, "message": alert.message, "created_at": alert.created_at} for alert in alerts]
    return JsonResponse(alert_data, safe=False)

def dashboard_view(request):
    return render(request, "dashboard.html") 


# views.py
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum




"""def get_sensor_data(request):
    # Obtén los datos de los últimos 5 minutos
    time_threshold = timezone.now() - timedelta(minutes=5)

    # Datos de cada sensor
    temp_data = SensorTemp.objects.filter(date__gte=time_threshold).values("date", "value")
    sonido_data = SensorSonido.objects.filter(date__gte=time_threshold).values("date", "value")
    luz_data = SensorLuz.objects.filter(date__gte=time_threshold).values("date", "value")
    
    # Formatear las fechas y los valores
    data = {
        "temp_timestamps": [entry["date"].strftime("%Y-%m-%d %H:%M:%S") for entry in temp_data],
        "temp_values": [entry["value"] for entry in temp_data],
        "sonido_timestamps": [entry["date"].strftime("%Y-%m-%d %H:%M:%S") for entry in sonido_data],
        "sonido_values": [entry["value"] for entry in sonido_data],
        "luz_timestamps": [entry["date"].strftime("%Y-%m-%d %H:%M:%S") for entry in luz_data],
        "luz_values": [entry["value"] for entry in luz_data],
    }
    return JsonResponse(data)"""
def get_sensor_data(request):
    # Obtén los datos de los últimos 5 minutos
    time_threshold = timezone.now() - timedelta(minutes=5)

    # Datos de cada sensor
    temp_data = SensorTemp.objects.filter(date__gte=time_threshold).values("date", "value")
    sonido_data = SensorSonido.objects.filter(date__gte=time_threshold).values("date", "value")
    luz_data = SensorLuz.objects.filter(date__gte=time_threshold).values("date", "value")

    # Obtener los tiempos del semáforo
    semaforo_data = Postura.objects.values('semaforo').annotate(total_tiempo=Sum('tiempo'))
    tiempos = { 'Verde': 0, 'Amarillo': 0, 'Rojo': 0 }
    for dato in semaforo_data:
        tiempos[dato['semaforo']] += dato['total_tiempo']

    
    # Formatear las fechas y los valores
    response_data = {
        "temp_timestamps": [entry["date"].strftime("%Y-%m-%d %H:%M:%S") for entry in temp_data],
        "temp_values": [entry["value"] for entry in temp_data],
        "sonido_timestamps": [entry["date"].strftime("%Y-%m-%d %H:%M:%S") for entry in sonido_data],
        "sonido_values": [entry["value"] for entry in sonido_data],
        "luz_timestamps": [entry["date"].strftime("%Y-%m-%d %H:%M:%S") for entry in luz_data],
        "luz_values": [entry["value"] for entry in luz_data],
        'semaforo_tiempos': tiempos,
    }
    return JsonResponse(response_data)

def sensors_view(request):
    return render(request, "get_sensorData.html")

def index(request):
    return render(request, 'index.html')

def buttons(request):
    return render(request, 'pages/ui-features/buttons.html')

def dropdowns(request):
    return render(request, 'pages/ui-features/dropdowns.html')

def typography(request):
    return render(request, 'pages/ui-features/typography.html')

def basic_elements(request):
    return render(request, 'pages/tables/basic_table.html')

def basic_tables(request):
    return render(request, 'pages/forms/basic_elements.html')

# Vista para el archivo ChartJs
def chart(request):
    return render(request, 'pages/charts/chartjs.html')

def mdi_view(request):
    return render(request, 'pages/icons/mdi.html')

# Nueva vista para Login
def login_view(request):
    return render(request, 'pages/samples/login.html')

# Nueva vista para Register
def register_view(request):
    return render(request, 'pages/samples/register.html')