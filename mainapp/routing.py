from django.urls import path
from .consumers import LogConsumer, PatientEventConsumer

websocket_urlpatterns = [
    path('ws/logs/', LogConsumer.as_asgi()),
    path('ws/patient-add/', PatientEventConsumer.as_asgi()),
]