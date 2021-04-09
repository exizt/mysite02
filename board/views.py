from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from math import ceil
from board.models import Board
from django.core.paginator import Paginator

LIST_COUNT = 10


def index(request):
    results = Board.objects.all().order_by('-reg_date')
    data = {
        'list': results
    }
    return render(request, 'board/index.html', data)


# 게시판 보기. (글 목록)
def index2(request):
    page = int(request.GET.get('p', '1'))

    if 'kwd' in request.GET:
        kwd = request.GET.get('kwd', '')
        # print("키워드 있음")
    else:
        kwd = ''

    # noinspection PyShadowingNames
    index = (page - 1) * LIST_COUNT
    results = Board.findall(index, LIST_COUNT, kwd)

    totalcount = Board.count(kwd)
    pagecount = ceil(totalcount/LIST_COUNT)
    curpage = page
    nextpage = curpage + 1 if curpage < pagecount else curpage
    prevpage = 1 if (curpage - 1) < 1 else curpage - 1

    # totalcount : 전체 글 수, listcount : 페이지당 글 갯수, pagecount : 페이징 수
    paginator = {
        'totalcount': totalcount,
        'listcount': LIST_COUNT,
        'pagecount': pagecount,
        'nextpage': nextpage,
        'prevpage': prevpage,
        'curpage': curpage,
        'paging': range(1, 6)
    }
    # 글 시작 번호
    startcount = totalcount - (curpage - 1) * LIST_COUNT
    #print(startcount)

    data = {
        'startcount': startcount,
        'list': results,
        'keyword': kwd,
        'baseurl': '/board',
        'paginator': paginator
    }
    return render(request, "board/index.html", data)


# 게시글 읽기
def view(request):
    postno = request.GET.get('no')
    if postno is None:
        return HttpResponse('잘못된 접근입니다.')

    result = Board.find(postno)
    if result is None:
        return HttpResponse('없는 게시글입니다.')

    data = {
        'post': result,
        'baseurl': '/board'
    }

    # 조회수 증가
    Board.increment_hit(postno)
    return render(request, "board/view.html", data)


# 글 쓰기
def writeform(request):
    authuser = request.session.get('authuser')
    if authuser is None:
        # 유저가 아닌 접근이므로. 비정상 접근이거나 세션 해제된 상태.
        return HttpResponseRedirect('/')

    data = {
        'baseurl': '/board'
    }
    return render(request, "board/writeform.html", data)


# 저장 처리
def write(request):
    authuser = request.session.get('authuser')
    if authuser is None:
        # 유저가 아닌 접근이므로. 비정상 접근이거나 세션 해제된 상태.
        return HttpResponseRedirect('/')

    title = request.POST.get('title', '')
    contents = request.POST.get('contents', '')

    # 저장 처리
    data = {
        'user_no': authuser['no'], 'title': title, 'contents': contents
    }
    ret = Board.insert(data)
    if ret != 1:
        return HttpResponse('오류 발생')

    return HttpResponseRedirect('/board/')
    # return HttpResponseRedirect('/board/view/?no=')


# 글 수정
def updateform(request):
    authuser = request.session.get('authuser')
    if authuser is None:
        # 유저가 아닌 접근이므로. 비정상 접근이거나 세션 해제된 상태.
        return HttpResponseRedirect('/')

    postno = request.GET.get('no')
    if postno is None:
        return HttpResponse('잘못된 접근입니다.')

    result = Board.find(postno)
    if result is None:
        return HttpResponse('없는 게시글입니다.')

    if result['user_no'] != authuser['no']:
        return HttpResponse('권한이 없습니다.')

    data = {
        'post': result,
        'baseurl': '/board'
    }
    return render(request, "board/updateform.html", data)


# 변경 처리
def update(request):
    authuser = request.session.get('authuser')
    if authuser is None:
        # 유저가 아닌 접근이므로. 비정상 접근이거나 세션 해제된 상태.
        return HttpResponseRedirect('/')

    postno = request.POST.get('no')
    if postno is None:
        return HttpResponse('잘못된 접근입니다.')

    result = Board.find(postno)
    if result is None:
        return HttpResponse('없는 게시글입니다.')

    if result['user_no'] != authuser['no']:
        return HttpResponse('권한이 없습니다.')

    title = request.POST.get('title', '')
    contents = request.POST.get('contents', '')

    data = {'title': title, 'contents': contents, 'no': postno}
    Board.update(data)

    return HttpResponseRedirect('/board/')


# 글 삭제 처리
def delete(request):
    authuser = request.session.get('authuser')
    if authuser is None:
        # 유저가 아닌 접근이므로. 비정상 접근이거나 세션 해제된 상태.
        return HttpResponseRedirect('/')

    postno = request.GET.get('no')
    if postno is None:
        return HttpResponse('잘못된 접근입니다.')

    result = Board.find(postno)
    if result is None:
        return HttpResponse('없는 게시글입니다.')

    if result['user_no'] != authuser['no']:
        return HttpResponse('권한이 없습니다.')

    Board.delete(postno)

    return HttpResponseRedirect('/board/')


def replyform(request):
    authuser = request.session.get('authuser')
    if authuser is None:
        # 유저가 아닌 접근이므로. 비정상 접근이거나 세션 해제된 상태.
        return HttpResponseRedirect('/')

    postno = request.GET.get('no')
    if postno is None:
        return HttpResponse('잘못된 접근입니다.')

    result = Board.find(postno)
    if result is None:
        return HttpResponse('없는 게시글입니다.')

    data = {
        'origin': result,
        'baseurl': '/board'
    }
    return render(request, 'board/replyform.html', data)


def reply(request):
    authuser = request.session.get('authuser')
    if authuser is None:
        # 유저가 아닌 접근이므로. 비정상 접근이거나 세션 해제된 상태.
        return HttpResponseRedirect('/')

    title = request.POST.get('title', '')
    contents = request.POST.get('contents', '')

    g_no = request.POST.get('g_no', 0)
    o_no = request.POST.get('o_no', 0)
    depth = request.POST.get('depth', 0)

    g_no = int(g_no)
    o_no = int(o_no) + 1
    depth = int(depth) + 1

    # 저장 처리
    data = {
        'user_no': authuser['no'], 'title': title, 'contents': contents,
        'g_no': g_no, 'o_no': o_no, 'depth': depth
    }
    ret = Board.reply(data)
    if ret != 1:
        return HttpResponse('오류 발생')

    return HttpResponseRedirect('/board/')
