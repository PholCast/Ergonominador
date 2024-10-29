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