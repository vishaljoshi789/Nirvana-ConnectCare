from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (
    HospitalView,
    WardView,
    UserView,
    StaffView,
    PatientView,
    LogsView,
    ConnectionView
)

urlpatterns = [
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('hospitals/', HospitalView.as_view(), name='hospital'),
    path('wards/', WardView.as_view(), name='ward'),
    path('user/', UserView.as_view(), name='user'),
    path('staff/', StaffView.as_view(), name='staff'),
    path('patient/', PatientView.as_view(), name='patient'),
    path('logs/', LogsView.as_view(), name='logs'),
    path('connections/', ConnectionView.as_view(), name='connection'),
]