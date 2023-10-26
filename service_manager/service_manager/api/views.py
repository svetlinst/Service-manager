from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets

from service_manager.api.serializers import ServiceOrderHeaderSerializer
from service_manager.main.models import ServiceOrderHeader
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated


class ListServiceOrderHeadersViewSet(viewsets.ModelViewSet):
    serializer_class = ServiceOrderHeaderSerializer
    queryset = ServiceOrderHeader.objects.all()
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
