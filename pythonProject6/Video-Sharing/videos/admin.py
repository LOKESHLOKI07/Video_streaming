from django.contrib import admin
from .models import Video
from .models import Machine, ProductionLog

@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):
    list_display = ('machine_name', 'machine_serial_no', 'time')

@admin.register(ProductionLog)
class ProductionLogAdmin(admin.ModelAdmin):
    list_display = ('cycle_no', 'unique_id', 'material_name', 'machine', 'start_time', 'end_time', 'duration')

admin.site.register(Video)
