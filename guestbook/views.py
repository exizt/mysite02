from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from guestbook.models import Guestbook


def index(request):
    results = Guestbook.objects.all().order_by('-reg_date')
    data = {
        'list': results
    }
    return render(request, 'guestbook/index.html', data)


def add(request):
    guestbook = Guestbook()

    guestbook.name = request.POST.get('name', '')
    guestbook.password = request.POST.get('password', '')
    guestbook.message = request.POST.get('message', '')

    guestbook.save()

    return HttpResponseRedirect('/guestbook/')


def deleteform(request):
    guestbook_id = request.GET.get('id')

    result = Guestbook.objects.get(id=guestbook_id)

    if not result:
        return HttpResponse('<h1>잘못된 접근입니다.</h1><a href="/guestbook01/">리스트로 가기</a>',
                            content_type='text/html; charset=utf-8')

    data = {
        'item': result
    }

    return render(request, 'guestbook/deleteform.html', data)


def delete(request):
    guestbook_id = request.POST.get('id')
    guestbook_pw = request.POST.get('password')

    guestbook = Guestbook.objects.filter(id=guestbook_id).filter(password=guestbook_pw)
    guestbook.delete()

    return HttpResponseRedirect('/guestbook/')

