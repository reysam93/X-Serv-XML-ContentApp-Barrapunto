from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseNotFound
from models import Page
from xmlbarrapunto import getNews
from django.core.cache import caches


cache = caches['default']


def updateNews(request):
    news = getNews()
    cache.set('news', news)
    return HttpResponse("News updated<br>")


@csrf_exempt
def processRequest(request, resource):
    if request.method == "GET":
        try:
            content = Page.objects.get(name=resource)
            news = cache.get('news')
            if news == None:
                news = getNews()
                cache.set('news', news)
            return HttpResponse(content.content + news)
        except Page.DoesNotExist:
            return HttpResponseNotFound(resource + " not found")
    elif request.method == "PUT":
        try:
            newPage = Page.objects.get(name=resource)
            newPage.page = request.body
        except Page.DoesNotExist:
            newPage = Page(name = resource, page = request.body)
        newPage.save()
        return HttpResponse(resource + " added to the list")
    else:
        return HttpResponse(status=403)
