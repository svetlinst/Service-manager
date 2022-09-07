from django.http import HttpResponse
from django.shortcuts import render


def get_index(request):
    return HttpResponse(request)
