from django.forms import ModelForm

from profileapp.models import Profile


class ProfileCreationForm(ModelForm): # modelform을 상속
    class Meta:
        model = Profile # 사용할 모델 지정
        fields = ['image', 'nickname', 'message'] # 사용할 필드 지정