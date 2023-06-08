from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Profile(models.Model):
    # OneToOneField, User와 Profile 객체를 1:1로 연결시켜줌
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    # upload_to : 서버에 들어온 Image를 저장시킬 위치 지정
    image = models.ImageField(upload_to='profile/', null=True)

    # unique : 객체 안에서 nickname는 1개여야 한다.(중복 x)
    nickname = models.CharField(max_length=20, unique=True, null=True)
    message = models.CharField(max_length=100, null=True)