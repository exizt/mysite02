from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

from user.models import User


# 회원 가입 폼
def joinform(request):
    return render(request, 'user/joinform.html')


# 회원 가입 성공시 보여줄 페이지
def joinsuccess(request):
    return render(request, 'user/joinsuccess.html', {})


# 회원 가입 처리
def join(request):
    name = request.POST.get('name', '')
    email = request.POST.get('email', '')
    password = request.POST.get('password')
    gender = request.POST.get('gender', '')

    if name == '' or name is None:
        return HttpResponse('잘못된 접근입니다.')

    if email == '' or email is None:
        return HttpResponse('잘못된 접근입니다.')

    if password == '' or password is None:
        return HttpResponse('잘못된 접근입니다.')

    if gender != 'female' and gender != 'male':
        return HttpResponse('잘못된 접근입니다.')

    user = User()
    user.name = name
    user.email = email
    user.password = password
    user.gender = gender
    user.save()

    return HttpResponseRedirect('/user/joinsuccess')


# 로그인 폼
def loginform(request):
    return render(request, 'user/loginform.html')


# 로그인 처리
def login(request):
    email = request.POST.get('email', '')
    password = request.POST.get('password', '')

    result = User.objects.get(email=email, password=password)
    # print(result)
    if result is None:
        return HttpResponseRedirect('/user/loginform?result=failed')
    else:
        request.session['authuser'] = {
            'id': result.id,
            'name': result.name
        }
        return HttpResponseRedirect('/')
        # return HttpResponse('ok')


# 로그아웃
# 세션을 없애고 리디렉션
def logout(request):
    del request.session['authuser']
    return HttpResponseRedirect('/')


# 회원정보수정 폼
def updateform(request):
    # Access Control(접근 제어)

    # 세션 체크 필요.
    authuser = request.session.get("authuser")
    if authuser is None:
        return HttpResponseRedirect('/')

    # print(authuser)
    # 세션에서 authuser.no 를 가져와서 쿼리
    # result = models.findbyno(authuser['no'])
    result = User.objects.get(id=authuser['id'])
    return render(request, 'user/updateform.html', {
        'result': result
    })


# 회원정보수정 처리
def update(request):
    authuser = request.session.get("authuser")
    if authuser is None:
        # 잘못된 접근이거나 로그인 해제 됨
        return HttpResponseRedirect('/')

    # 파라미터
    name = request.POST.get('name', '')
    password = request.POST.get('password', '')
    gender = request.POST.get('gender', '')

    if name == '' or name is None:
        return HttpResponse('잘못된 접근입니다.')

    if gender != 'female' and gender != 'male':
        return HttpResponse('잘못된 접근입니다.')

    user = User.objects.get(id=authuser['id'])
    user.name = name
    if len(password) > 1:
        user.password = password
    user.gender = gender
    user.save()

    # print(authuser)
    # models.update(authuser['no'], name, gender, password)

    # new_authuser = models.findbyno(authuser['no'])
    new_authuser = User.objects.get(id=authuser['id'])

    request.session['authuser'] = {
        'id': new_authuser.id,
        'name': new_authuser.name
    }
    # print(request.session['authuser'])
    # return HttpResponse('ok')
    return HttpResponseRedirect('/user/updateform')
