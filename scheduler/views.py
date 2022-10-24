from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    response_text = 'Welcome to the ticket scheduler, you must be looking for the <a href="https://ticketscheduler.t6f.co.za/admin/">admin</a> page.'
    return HttpResponse(response_text)