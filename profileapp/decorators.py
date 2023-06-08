from django.http import HttpResponseForbidden

from profileapp.models import Profile


def profile_ownership_required(func):
    def decorated(request, *args, **kwargs):
        profile = Profile.objects.get(pk=kwargs['pk']) # 요청을 받은 pk키를 가지고 있는 유저 오브젝트
        if not profile.user == request.user: # user가 request로 받은 user가 아니면 실행
            return HttpResponseForbidden()
        return func(request, *args, **kwargs )
    return decorated