from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Hospital, Ward, User, Staff, Patient, Logs, Connection
from .serializers import (
    HospitalSerializer,
    WardSerializer,
    UserSerializer,
    StaffSerializer,
    StaffUserSerializer,
    PatientSerializer,
    LogsSerializer,
    ConnectionSerializer,
    UserInfoSerializer
)
from rest_framework.permissions import AllowAny
from django.contrib.auth.hashers import make_password

class HospitalView(APIView):
    def get(self, request):
        hospitals = Hospital.objects.all()
        serializer = HospitalSerializer(hospitals, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = HospitalSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class WardView(APIView):
    def get(self, request):
        wards = Ward.objects.all()
        serializer = WardSerializer(wards, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = WardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        user = request.user
        serializer = UserInfoSerializer(user)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        if "password" in data:
            data["password"] = make_password(data["password"])

        serializer = UserSerializer(data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StaffView(APIView):
    def get(self, request):
        staff = Staff.objects.filter(ward=request.GET.get('ward')).filter(hospital=request.user.role.hospital)
        serializer = StaffUserSerializer(staff, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        data['user'] = User.objects.get(username=data['user']).id
        data['hospital'] = request.user.role.hospital.id
        serializer = StaffSerializer(data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PatientView(APIView):
    def get(self, request):
        patients = Patient.objects.all()
        serializer = PatientSerializer(patients, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        data['user'] = User.objects.get(username=data['user']).id
        data['hospital'] = request.user.role.hospital.id
        serializer = PatientSerializer(data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogsView(APIView):
    def get(self, request):
        logs = Logs.objects.all()
        serializer = LogsSerializer(logs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = LogsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ConnectionView(APIView):
    def get(self, request):
        connections = Connection.objects.all()
        serializer = ConnectionSerializer(connections, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ConnectionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)