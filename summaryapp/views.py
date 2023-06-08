from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView

from khj.crawling import get_news
from summaryapp.decorators import account_ownership_required
from summaryapp.forms import AccountUpdateForm
from summaryapp.models import Summary, Crawling

has_ownership = [account_ownership_required, login_required]
# Create your views here.

@login_required(login_url='/summarys/login/')
def index(request):
    if request.method == 'POST':
        temp = request.POST.get('summary_input')
        new_summary = Summary()
        new_summary.text = temp
        new_summary.save()
        return render(request, 'summaryapp/index.html', context={'summary_output' : new_summary})
    else:
        return render(request, 'summaryapp/index.html', context={'text' : 'get Method!'})

def crawling_test(request):
    global crawling_output1, crawling_output2, crawling_output3
    if request.method == 'POST':
        subs = request.POST.get('crawling_input')
        crawling_df = get_news(subs)
        for i in range(0, crawling_df.shape[0]):
            if i != 1:
                row = crawling_df.iloc[i]
                crawling_output1 = row['press']
                crawling_output2 = row['title']
                crawling_output3 = row['article']
            else:
                break
        new_crawling = Crawling(press=crawling_output1, title=crawling_output2, article=crawling_output3)
        new_crawling.text = crawling_output3
        new_crawling.save()

        return render(request, 'summaryapp/index.html', context={'crawling_data' : new_crawling})
    else:
        return render(request, 'summaryapp/index.html', context={'text' : '내용이 없습니다.'})

class AccountCreateView(CreateView):
    model = User
    form_class = UserCreationForm # User 모델을 만들 때 사용할 Form 가져오기
    success_url = reverse_lazy('summaryapp:index') # 계정 생성 성공시 어느 경로로 연결을 할것인지 지정
    template_name = 'summaryapp/create.html' # 어느 HTML을 사용하요 Form을 볼지 지정


class AccountDetailView(DetailView):
    model = User
    context_object_name = 'target_user'
    template_name = 'summaryapp/detail.html'


@method_decorator(has_ownership, 'get') # 일반 함수에 사용하는 데코레이터를 메소드에서 사용 할 수 있도록 변환
@method_decorator(has_ownership, 'post') # 일반 함수에 사용하는 데코레이터를 메소드에서 사용 할 수 있도록 변환
class AccountUpdateView(UpdateView):
    model = User
    context_object_name = 'target_user'
    form_class = AccountUpdateForm # User 모델을 만들 때 사용할 Form 가져오기
    success_url = reverse_lazy('summaryapp:index') # 계정 생성 성공시 어느 경로로 연결을 할것인지 지정
    template_name = 'summaryapp/update.html' # 어느 HTML을 사용하요 Form을 볼지 지정


@method_decorator(has_ownership, 'get') # 일반 함수에 사용하는 데코레이터를 메소드에서 사용 할 수 있도록 변환
@method_decorator(has_ownership, 'post') # 일반 함수에 사용하는 데코레이터를 메소드에서 사용 할 수 있도록 변환
class AccountDeleteView(DeleteView):
    model = User
    context_object_name = 'target_user'
    success_url = reverse_lazy('summaryapp:login')  # 계정 생성 성공시 어느 경로로 연결을 할것인지 지정
    template_name = 'summaryapp/delete.html'  # 어느 HTML을 사용하요 Form을 볼지 지정
