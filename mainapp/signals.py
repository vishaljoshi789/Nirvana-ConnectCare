from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Logs, Connection, Patient
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import json

@receiver(post_save, sender=Logs)
def notify_connected_users(sender, instance, **kwargs):
    channel_layer = get_channel_layer()
    patient_user = instance.patient.user  # Get the Patient's User

    # Find all users connected to the patient
    connections = Connection.objects.filter(user1=patient_user) | Connection.objects.filter(user2=patient_user)

    for connection in connections:
        # Determine the other user in the connection
        other_user = connection.user2 if connection.user1 == patient_user else connection.user1

        # Send WebSocket notification to the other user
        async_to_sync(channel_layer.group_send)(
            f"user_{other_user.id}",  # Unique group name for each user
            {
                "type": "send_log_update",  # Custom event name
                "data": {
                    "log_id": instance.id,
                    "patient": instance.patient.user.name,
                    "log": instance.log,
                    "updated_by": instance.updated_by.name,
                    "updated_on": instance.updated_on.strftime('%Y-%m-%d %H:%M:%S'),
                }
            }
        )

@receiver(post_save, sender=Patient)
def notify_admission_discharge(sender, instance, created, **kwargs):
    channel_layer = get_channel_layer()

    if created:
        # Patient admitted for the first time
        event_type = "admitted"
        message = f"{instance.user.name} has been admitted to ward {instance.ward}."
    elif instance.admit and not instance.discharge:
        # Patient re-admitted
        event_type = "admitted"
        message = f"{instance.user.name} has been re-admitted to ward {instance.ward}."
    elif instance.discharge:
        # Patient discharged
        event_type = "discharged"
        message = f"{instance.user.name} has been discharged."

    # Find all users connected to the patient
    patient_user = instance.user
    connections = Connection.objects.filter(user1=patient_user) | Connection.objects.filter(user2=patient_user)

    for connection in connections:
        # Determine the other user in the connection
        other_user = connection.user2 if connection.user1 == patient_user else connection.user1

        # Send WebSocket notification to the other user
        async_to_sync(channel_layer.group_send)(
            f"user_{other_user.id}",  # Unique group name for each user
            {
                "type": "send_patient_event",  # Custom event name
                "data": {
                    "event_type": event_type,
                    "patient_name": instance.user.name,
                    "ward": instance.ward,
                    "admit": instance.admit.strftime('%Y-%m-%d %H:%M:%S') if instance.admit else None,
                    "discharge": instance.discharge.strftime('%Y-%m-%d %H:%M:%S') if instance.discharge else None,
                    "message": message,
                }
            }
        )