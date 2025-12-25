from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

# Create your views here.
def home(request):
	return HttpResponse("API Backend for Threat Monitoring Service")