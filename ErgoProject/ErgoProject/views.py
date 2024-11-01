from django.http import JsonResponse
from mqttApp.models import Alert, SensorLuz, SensorSonido, SensorTemp, Postura
from django.shortcuts import render
from django.db.models import Max, Sum
from datetime import datetime, timedelta

# def get_alerts(request):
#     # Aquí podríamos filtrar por alertas recientes si es necesario
#     alerts = Alert.objects.order_by('-created_at')[:10]  # Últimas 10 alertas
#     alert_data = [{"type_alert": alert.type_alert, "message": alert.message, "created_at": alert.created_at} for alert in alerts]
#     return JsonResponse(alert_data, safe=False)

def get_alerts(request):
    # Obtener la última alerta de cada tipo usando Max sobre el campo `created_at`
    # latest_alerts = Alert.objects.values('type_alert').annotate(latest_created_at=Max('created_at'))
    latest_alerts = Alert.objects.filter(seen=False).values('type_alert').annotate(latest_created_at=Max('created_at'))

    # Filtrar las alertas para obtener los detalles completos de las últimas de cada tipo
    alerts = Alert.objects.filter(
        created_at__in=[alert['latest_created_at'] for alert in latest_alerts]
    )

    # Obtener la última entrada de Postura
    latest_postura = Postura.objects.order_by('-created_at').first()

    # Serializar los datos para cada alerta en el formato requerido
    # alert_data = {
    #     alert.type_alert: {
    #         "type_alert": alert.type_alert,
    #         "message": alert.message,
    #         "created_at": alert.created_at.strftime("%H:%M:%S")
    #     }
    #     for alert in alerts
    # }
    alert_data = {
    alert.type_alert: {
        "type_alert": alert.type_alert,
        "message": alert.message,
        "created_at": alert.created_at.strftime("%H:%M:%S"),
        "seen": alert.seen  # Añadir el campo visto
    }
    for alert in alerts
    }

    alerts.update(seen=True)
    # Agregar la última postura si existe usando los campos del modelo
    if latest_postura:
        alert_data['Postura'] = {
            "tiempo": latest_postura.tiempo,
            "semaforo": latest_postura.semaforo,
            "created_at": latest_postura.created_at.strftime("%H:%M:%S")
        }

    return JsonResponse(alert_data, safe=False)


def dashboard_view(request):
    return render(request, "dashboard.html") 



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
    time_threshold = time_threshold = datetime.now() - timedelta(minutes=5)

    # Datos de cada sensor
    temp_data = SensorTemp.objects.filter(date__gte=time_threshold).values("date", "value")
    sonido_data = SensorSonido.objects.filter(date__gte=time_threshold).values("date", "value")
    luz_data = SensorLuz.objects.filter(date__gte=time_threshold).values("date", "value")

    # Obtener los tiempos del semáforo
    semaforo_data = Postura.objects.values('semaforo').annotate(total_tiempo=Sum('tiempo'))
    tiempos = { 'Verde': 0, 'Amarillo': 0, 'Rojo': 0 }
    
    verde_count = Postura.objects.filter(semaforo='Verde').count()

    # for dato in semaforo_data:
    #     tiempos[dato['semaforo']] += dato['total_tiempo']
    for dato in semaforo_data:
        if dato['semaforo'] == 'AmarilloVerde':
            tiempos['Amarillo'] += dato['total_tiempo']
        else:
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
        'verde_count': verde_count-1,  # Añadir el conteo de semáforos en verde
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