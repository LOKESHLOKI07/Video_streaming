from django.db import models
from django.utils import timezone
from django.core.validators import FileExtensionValidator

class Video(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    video_file = models.FileField(upload_to='uploads/video_files',
                                  validators=[FileExtensionValidator(allowed_extensions=['mp4'])])
    thumbnail = models.FileField(upload_to='uploads/thumbnails',
                                 validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg'])])
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
from django.db import models

class Machine(models.Model):
    machine_name = models.CharField(max_length=100)
    machine_serial_no = models.CharField(max_length=100)
    time = models.DateTimeField(auto_now_add=True)

class ProductionLog(models.Model):
    cycle_no = models.CharField(max_length=100)
    unique_id = models.CharField(max_length=100)
    material_name = models.CharField(max_length=100)
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    duration = models.FloatField()
    actual_output = models.IntegerField(default=0)
    good_products = models.IntegerField(default=0)
