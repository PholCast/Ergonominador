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

class SensorSonido(SensorBase):
    pass

class SensorLuz(SensorBase):
    pass
