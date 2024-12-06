from django.contrib import admin
from .models import User, Hospital, Ward, Staff, Patient, Logs, Connection
# Register your models here.

admin.site.register(User)
admin.site.register(Hospital)
admin.site.register(Ward)
admin.site.register(Staff)
admin.site.register(Patient)
admin.site.register(Logs)
admin.site.register(Connection)
