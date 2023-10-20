from django.db import models
import uuid

class PCPart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=3, choices=[('CPU', 'CPU'), ('GPU', 'GPU')]) # These are the only valid options
    release_date = models.IntegerField(default=0)  # Store release date as Unix epoch timestamp
    core_clock = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    boost_clock = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # Optional field
    clock_unit = models.CharField(max_length=4, default="GHz")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    TDP = models.IntegerField(default=0)
    part_no = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.name + "   " + self.type
