from django.db import models

class SensorBase(models.Model):
    value = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"Sensor ID: {self.sensor_id}, Value: {self.value}, Date: {self.date}"


class SensorTemp(SensorBase):
    pass
#sensor de ultrasonido
class SensorSonido(SensorBase):
    pass

class SensorLuz(SensorBase):
    pass

class Alert(models.Model):
    type_alert = models.CharField(max_length=50) #Distancia, Postura, Temperatura, luz
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type_alert} -- {self.message} -- {self.created_at}"  # Asegúrate de que la cadena esté cerrada

class Postura(models.Model):
    tiempo = models.IntegerField()
    semaforo = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.tiempo}s - {self.semaforo}"