from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render

from .models import UserProfile

def index(request):
    context = {
        'title': 'Главная страница',
        'count': UserProfile.objects.count(),
        'users': UserProfile.objects.all().prefetch_related('skills', 'skills__skill', 'gallery')[:4],
    }
    return render(request, 'users/index.html', context)

def user_list(request):
    context = {
        'title': 'Список',
        'users': Paginator(UserProfile.objects.all().prefetch_related('skills', 'skills__skill', 'gallery'), 10).get_page(request.GET.get('page')),
    }
    return render(request, 'users/user_list.html', context)

@login_required
def user_detail(request, id):
    user = UserProfile.objects.prefetch_related('skills', 'skills__skill', 'gallery').select_related('desk').get(id=id)
    context = {
        'title': f'{user.name} {user.family}',
        'user': user,
    }
    return render(request, 'users/user_detail.html', context)