from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return HttpResponse("Welcome to the ticket scheduler, try the <a href='https://ticketscheduler.three6five.co.za>admin</a> url.")