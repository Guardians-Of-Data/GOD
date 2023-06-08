from django.contrib.auth.models import User
from django.http import HttpResponseForbidden


def account_ownership_required(func):
    def decorated(request, *args, **kwargs):
        user = User.objects.get(pk=kwargs['pk']) # 요청을 받은 pk키를 가지고 있는 유저 오브젝트
        if not user == request.user: # user가 request로 받은 user가 아니면 실행
            return HttpResponseForbidden()
        return func(request, *args, **kwargs )
    return decorated