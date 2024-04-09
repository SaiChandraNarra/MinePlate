from django.db import models



class ScannedVehicle(models.Model):
    time = models.TimeField()
    date = models.DateField()
    image = models.ImageField(upload_to='scanned_images/')
    number_plate = models.CharField(max_length=100)
    status = models.CharField(max_length=100)

    def __str__(self):
        return f"Scanned Vehicle - {self.number_plate}"


# Create your models here.
