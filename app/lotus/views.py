from django.shortcuts import render
from rest_framework import viewsets

from lotus.models import Computador
from lotus.serializers import ComputadorListSerializer

# Create your views here.


class ComputadoresViewSet(viewsets.ModelViewSet):
    """ViewSet de computadores."""

    queryset = Computador.objects.all()
    serializer_class = ComputadorListSerializer
