from django.shortcuts import render, HttpResponse

from . import models


def index(request):
    response = {

    }
    
    for section in models.Section.objects.all():
        for thread in section.threads.all():
            for post in thread.posts.all():
                if section not in response.keys():
                    response[section] = {}
                if thread not in response[section].keys():
                    response[section][thread] = []
                    
                response[section][thread].append(post)

    return HttpResponse(response.__str__())
