from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseNotFound
from models import Page
from xmlbarrapunto import getNews
import codecs


def updateNews(request):
    getNews()
    return HttpResponse ("News updated<br>")

@csrf_exempt
def processRequest(request, resource):
    if request.method == "GET":
        try:
            content = Page.objects.get(name=resource)
            try:
                parsedFile = codecs.open("barrapunto.txt", "r", "utf-8")
            except IOError:
                updateNews(request)
                parsedFile = codecs.open("barrapunto.txt", "r", "utf-8")
            news = "<br><hr>" + parsedFile.read()
            return HttpResponse(content.content + news)
        except Page.DoesNotExist:
            return HttpResponseNotFound(resource + " not found")
    elif request.method == "PUT":
        newContent = Page(name=resource, content=request.body)
        newContent.save()
        return HttpResponse(resource + " added to the list")
    else:
        return HttpResponse(status=403)
